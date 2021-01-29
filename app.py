from flask import Flask
from flask_cors import CORS

from nauron import Sauron, ServiceConf
from bert_ner_nazgul import BertNerNazgul

# Define Flask application
app = Flask(__name__)
CORS(app)

bert_conf = ServiceConf(name='ner',
                        endpoint='/api/bertner',
                        nazguls= {'public': BertNerNazgul()})

# Define API endpoints
app.add_url_rule(bert_conf.endpoint, view_func=Sauron.as_view(bert_conf.name, bert_conf))


if __name__ == '__main__':
    app.run()