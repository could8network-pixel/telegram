import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("8656583035:AAEuvWLHdy_LbMw5VgP4L7dNvbYqSU7jNZA")
USER_ID = os.getenv(" 476093481")
API_TOKEN = os.getenv("5be6a2daa545f53d80d484cc29f4b979")
GEO_CODE = os.getenv("9.683,76.433")
PINCODE = os.getenv("686607")

ADMIN_ID = 476093481

API_URL = "https://foursaeasy.com/API/TransactionAPI"

OPERATORS = {
    "Airtel": "3",
    "Jio": "116",
    "VI": "37",
    "BSNL STV": "5",
    "BSNL Talktime": "4"
}
