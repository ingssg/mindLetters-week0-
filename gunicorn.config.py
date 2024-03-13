# gunicorn.conf.py
# https://stackoverflow.com/questions/68622148/running-flask-app-with-gunicorn-and-environment-variables
# gunicorn --bind 0.0.0.0:5001 --config gunicorn.config.py wsgi:app -t 150
import os
from dotenv import load_dotenv

for env_file in ('.env',):
    env = os.path.join(os.getcwd(), env_file)
    if os.path.exists(env):
        load_dotenv(env)
