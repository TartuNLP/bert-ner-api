import logging
from collections import Counter

from typing import Dict, Any

import torch
import stanza
from transformers import BertTokenizer, BertForTokenClassification

from nauron import Response, Nazgul, MQConsumer
from marshmallow import Schema, fields, ValidationError
import pika

import settings

logger = logging.getLogger(settings.MQ_EXCHANGE)

class BertRequestSchema(Schema):
    text = fields.Str()

class BertNerNazgul(Nazgul):
    def __init__(self, stanza_location: str = "models/stanza_model", bert_location: str = "models/ner_bert"):
        self.schema = BertRequestSchema
        self.tokenizer = stanza.Pipeline(lang='et', dir=stanza_location, processors='tokenize', logging_level='WARN')
        self.bertner = BertForTokenClassification.from_pretrained(bert_location, return_dict=True)
        self.labelmap = {0: 'B-LOC', 1: 'B-ORG', 2: 'B-PER', 3: 'I-LOC', 4: 'I-ORG', 5: 'I-PER', 6: 'O'}
        self.bert_tokenizer = BertTokenizer.from_pretrained(bert_location)

    def process_request(self, body: Dict[str, Any], _: str = None) -> Response:
        try:
            body = self.schema().load(body)
            doc = self.tokenizer(body["text"])
            extracted_data = doc.to_dict()
            sentences = []
            for sentence in extracted_data:
                sentence_collected = []
                for word in sentence:
                    text = word.get('text')
                    sentence_collected.append(text)
                sentences.append(sentence_collected)
            tagged_sentences = []
            for sentence in sentences:
                entities = self.predict(sentence)
                words = []
                for word, entity in zip(sentence, entities):
                    subresult = {'word': word, 'ner': entity}
                    words.append(subresult)
                tagged_sentences.append(words)
            return Response({"result":tagged_sentences}, mimetype="application/json")
        except ValidationError as error:
            return Response(content=error.messages, http_status_code=400)
        except ValueError:
            return Response(http_status_code=413,
                            content='Input is too long.')

    def predict(self, sentence: list) -> list:
        grouped_inputs = [torch.LongTensor([self.bert_tokenizer.cls_token_id])]
        subtokens_per_token = []
        for token in sentence:
            tokens = self.bert_tokenizer.encode(
                token,
                return_tensors="pt",
                add_special_tokens=False,
            ).squeeze(axis=0)
            grouped_inputs.append(tokens)
            subtokens_per_token.append(len(tokens))

        grouped_inputs.append(torch.LongTensor([self.bert_tokenizer.sep_token_id]))

        flattened_inputs = torch.cat(grouped_inputs)
        flattened_inputs = torch.unsqueeze(flattened_inputs, 0)
        predictions_tensor = self.bertner(flattened_inputs)[0]
        predictions_tensor = torch.argmax(predictions_tensor, dim=2)[0]
        preds = predictions_tensor[1:-1]
        predictions = [self.labelmap.get(int(pred)) for pred in preds]
        aligned_predictions = []
        ptr = 0
        for size in subtokens_per_token:
            group = predictions[ptr:ptr + size]
            aligned_predictions.append(group)
            ptr += size
        predicted_labels = []
        previous = 'O'
        for token, prediction_group in zip(sentence, aligned_predictions):
            label = Counter(prediction_group).most_common(1)[0][0]
            base = label.split('-')[-1]
            if (previous == 'O' or previous.split('-')[-1] != base) and label.startswith('I'):
                label = 'B-' + base
            previous = label
            predicted_labels.append(label)
        return predicted_labels


if __name__ == "__main__":
    mq_parameters = pika.ConnectionParameters(host=settings.MQ_HOST,
                                              port=settings.MQ_PORT,
                                              credentials=pika.credentials.PlainCredentials(
                                                  username=settings.MQ_USERNAME,
                                                  password=settings.MQ_PASSWORD))

    service = MQConsumer(nazgul=BertNerNazgul(),
                         connection_parameters=mq_parameters,
                         exchange_name=settings.MQ_EXCHANGE,
                         queue_name=settings.MQ_QUEUE_NAME)
    service.start()
