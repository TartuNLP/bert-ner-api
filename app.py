import logging
from flask_cors import CORS

from webargs import fields
from webargs.flaskparser import use_args
from nauron import Nauron

import settings
from bert_ner_worker import BertNerWorker

logger = logging.getLogger("gunicorn.error")

# Define application
app = Nauron(__name__)
CORS(app)

ner = app.add_service(name='ner')

ner.add_worker(worker=BertNerWorker(stanza_location=settings.STANZA_PATH,
                                    bert_location=settings.BERT_PATH))

BODY = {
    "text": fields.Str(required=True)
}


@app.post('/bert/v1/ner')
@use_args(BODY, location="json")
def predict(body):
    response = ner.process_request(content=body)
    return response


if __name__ == '__main__':
    app.run()
