from pathlib import Path
from configparser import ConfigParser

_config = ConfigParser()
_config.read("config/config.ini")

STANZA_PATH = _config['models']['stanza']
BERT_PATH = _config['models']['bert']

Path("logs/").parents[0].mkdir(parents=True, exist_ok=True)