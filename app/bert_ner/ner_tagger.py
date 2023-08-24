import logging
from collections import Counter

from typing import Dict, Any, Optional

import torch
import stanza
from transformers import BertTokenizer, BertForTokenClassification

from app import ner_config
from . import ResponseModel, RequestModel

logger = logging.getLogger("ner")


class NERTagger:
    def __init__(self, stanza_location: str, ner_hf: str):
        self.tokenizer = stanza.Pipeline(lang='et', dir=stanza_location, processors='tokenize', logging_level='WARN')
        self.bert = BertForTokenClassification.from_pretrained(ner_hf, return_dict=True)
        self.labelmap = {0: 'B-LOC', 1: 'B-ORG', 2: 'B-PER', 3: 'I-LOC', 4: 'I-ORG', 5: 'I-PER', 6: 'O'}
        self.bert_tokenizer = BertTokenizer.from_pretrained(ner_hf)

    def process_request(self, body: RequestModel) -> ResponseModel:
        doc = self.tokenizer(body.text)
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
            entities = self._predict(sentence)
            words = []
            for word, entity in zip(sentence, entities):
                sub_result = {'word': word, 'ner': entity}
                words.append(sub_result)
            tagged_sentences.append(words)
        response = ResponseModel(result=tagged_sentences)
        return response

    def _predict(self, sentence: list) -> list:
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
        predictions_tensor = self.bert(flattened_inputs)[0]
        predictions_tensor = torch.argmax(predictions_tensor, dim=2)[0]
        predictions = predictions_tensor[1:-1]
        predictions = [self.labelmap.get(int(pred)) for pred in predictions]
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

ner_tagger = NERTagger(stanza_location=ner_config.stanza_path, ner_hf=ner_config.ner_hf)