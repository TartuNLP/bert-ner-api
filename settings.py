import logging.config
from os import environ
from pathlib import Path
from typing import Tuple
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
import pika
from dotenv import load_dotenv

def _load_config() -> Tuple[ConfigParser, str]:
    parser = ArgumentParser()
    parser.add_argument('--config-file', type=FileType('r'), default='config/config.ini',
                        help="Path to config file.")
    parser.add_argument('--log-config', type=FileType('r'), default='config/logging.ini',
                        help="Path to log config file.")
    args = parser.parse_known_args()[0]

    config = ConfigParser()
    config.read(args.config_file.name)
    return config, args.log_config.name


_config, _log_config = _load_config()
Path("logs/").mkdir(parents=True, exist_ok=True)
logging.config.fileConfig('config/logging.ini')

STANZA_PATH = _config['models']['stanza']
BERT_PATH = _config['models']['bert']

load_dotenv("config/.env")
load_dotenv("config/sample.env")

MQ_PARAMS = pika.ConnectionParameters(
    host=environ.get('MQ_HOST'),
    port=int(environ.get('MQ_PORT')),
    credentials=pika.credentials.PlainCredentials(username=environ.get('MQ_USERNAME'),
                                                  password=environ.get('MQ_PASSWORD')))

SERVICE_NAME = _config['rabbitmq']['exchange']
ROUTING_KEY = _config['rabbitmq']['queue_name']
ALT_ROUTES = eval(_config['rabbitmq']['alt_routes'])