from os import environ
from pathlib import Path
from configparser import ConfigParser
from dotenv import load_dotenv
import pika

_config = ConfigParser()
_config.read("config/config.ini")

load_dotenv("config/.env")
load_dotenv("config/sample.env")

Path("logs/").parents[0].mkdir(parents=True, exist_ok=True)

MQ_PARAMS = pika.ConnectionParameters(
    host=environ.get('MQ_HOST'),
    port=int(environ.get('MQ_PORT')),
    credentials=pika.credentials.PlainCredentials(username=environ.get('MQ_USERNAME'),
                                                  password=environ.get('MQ_PASSWORD')))

MESSAGE_TIMEOUT = int(environ.get('GUNICORN_TIMEOUT', '30')) * 1000

SERVICE_NAME = _config['general']['service']
