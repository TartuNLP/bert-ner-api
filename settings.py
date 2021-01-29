import logging.config
from os import environ
from dotenv import load_dotenv

logging.config.fileConfig('config/logging.conf')

load_dotenv("config/.env")

MQ_HOST = environ.get('MQ_HOST')
MQ_PORT = environ.get('MQ_PORT')
MQ_USERNAME = environ.get('MQ_USERNAME')
MQ_PASSWORD = environ.get('MQ_PASSWORD')
MQ_EXCHANGE = environ.get('MQ_EXCHANGE')
MQ_QUEUE_NAME = environ.get('MQ_QUEUE_NAME')