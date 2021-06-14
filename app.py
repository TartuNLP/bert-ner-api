import logging
from flask_cors import CORS

from webargs import fields
from webargs.flaskparser import use_args
from nauron import Nauron

import settings

logger = logging.getLogger("gunicorn.error")

# Define application
app = Nauron(__name__, mq_parameters=settings.MQ_PARAMS, timeout=settings.MESSAGE_TIMEOUT)
CORS(app)

ner = app.add_service(name='ner', remote=True)

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
