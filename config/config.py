import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")
ES_INDEX=os.environ.get("ES_INDEX")
ES_URL= os.environ.get("ES_URL")
