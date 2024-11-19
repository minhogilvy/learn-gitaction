import os
from dotenv import load_dotenv
load_dotenv()

MODEL_KEY = os.environ.get('MODEl_KEY', 'subscribe')
MODEL_TOKEN = os.environ.get('MODEl_TOKEN', '1234')