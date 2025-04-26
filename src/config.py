# config.py
from libraries import load_dotenv, os, find_dotenv

# load .env from project root
load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY in .env")

# set it for any library that reads os.environ
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
