# Gunicorn configuration file.
# This file can be used from the Gunicorn cli with the ``-c`` paramater.
# Eg. ``gunicorn -c <config_file>``
import multiprocessing
import os

bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1

for k,v in os.environ.items():
    if k.startswith("GUNICORN_"):
        key = k.split('_', 1)[1].lower()
        locals()[key] = v

