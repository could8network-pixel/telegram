from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv
from config import ADMIN_ID
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

MOBILE, OPERATOR, AMOUNT = range(3)

OPERATORS = [
    ["Airtel", "Jio"],
    ["VI", "BSNL"],
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ You are not authorized.")
        return

    await update.message.reply_text(
        "👋 Welcome to Recharge Bot\n\n"
        "Type /recharge to start."
    )

async def recharge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ You are not authorized.")
        return

    await update.message.reply_text(
        "📱 Enter Mobile Number:"
    )

    return MOBILE

async def mobile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mobile"] = update.message.text

    keyboard = ReplyKeyboardMarkup(
        OPERATORS,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "📶 Select Operator:",
        reply_markup=keyboard
    )

    return OPERATOR

async def operator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["operator"] = update.message.text

    await update.message.reply_text(
        "💰 Enter Amount:",
        reply_markup=ReplyKeyboardRemove()
    )

    return AMOUNT
    import requests
import uuid
from config import USER_ID, API_TOKEN, GEO_CODE, PINCODE, API_URL

SP_KEYS = {
    "Airtel": "3",
    "Jio": "116",
    "VI": "37",
    "BSNL": "4"
}

async def amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    amount = update.message.text

    mobile = context.user_data["mobile"]
    operator = context.user_data["operator"]

    params = {
        "UserID": USER_ID,
        "Token": API_TOKEN,
        "Account": mobile,
        "Amount": amount,
        "SPKey": SP_KEYS[operator],
        "APIRequestID": str(uuid.uuid4()),
        "Optional1": "",
        "Optional2": "",
        "Optional3": "",
        "Optional4": "",
        "GEOCode": GEO_CODE,
        "CustomerNumber": mobile,
        "Pincode": PINCODE,
        "Format": "1"
    }

    try:
        response = requests.get(API_URL, params=params, timeout=30)
        data = response.json()

        if str(data.get("STATUS")) == "2":
            await update.message.reply_text(
                f"✅ Recharge Success\n\n"
                f"Mobile: {mobile}\n"
                f"Amount: ₹{amount}\n"
                f"RPID: {data.get('RPID')}"
            )
        else:
            await update.message.reply_text(
                f"❌ Recharge Failed\n"
                f"{data.get('MSG')}"
            )

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("recharge", recharge)],
    states={
        MOBILE: [MessageHandler(filters.TEXT & ~filters.COMMAND, mobile)],
        OPERATOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, operator)],
        AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, amount)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(conv_handler)
app.add_handler(CommandHandler("start", start))
app.add_handler(conv_handler)

print("Bot is running...")
app.run_polling()
