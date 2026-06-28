mport os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")
API_TOKEN = os.getenv("API_TOKEN")
GEO_CODE = os.getenv("GEO_CODE")
PINCODE = os.getenv("PINCODE")

API_URL = "https://foursaeasy.com/API/TransactionAPI"

OPERATORS = {
    "Airtel": "3",
    "Jio": "116",
    "VI": "37",
    "BSNL STV": "5",
    "BSNL Talktime": "4"
