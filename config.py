from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = True if os.getenv("DEBUG") == "1" else False
