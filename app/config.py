import os
from dotenv import load_dotenv

load_dotenv()

START_PAGE = int(os.getenv("START_PAGE", 1))
END_PAGE = int(os.getenv("END_PAGE", 10))
LINK_OUTPUT = os.getenv("LINK_OUTPUT", "data/linkes_first.txt")
QA_OUTPUT = os.getenv("QA_OUTPUT", "data/output.json")
LISTING_URL = os.getenv("LISTING_URL")
