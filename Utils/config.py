import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
