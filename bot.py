import os
import uuid
import logging
import requests
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ConversationHandler, ContextTypes, filters,
)
from config import ADMIN_ID, USER_ID, API_TOKEN, GEO_CODE, PINCODE, API_URL, OPERATORS

logging.basicConfig(level=logging.INFO)
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

MOBILE, OPERATOR, AMOUNT = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔️ You are not authorized.")
        return
    await update.message.reply_text("👋 Welcome to Recharge Bot.\n\nType /recharge to start.")

async def recharge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔️ You are not authorized.")
        return ConversationHandler.END
    await update.message.reply_text("📱 Enter Mobile Number:")
    return MOBILE

async def mobile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mobile"] = update.message.text
    names=list(OPERATORS.keys())
    kb=[names[i:i+2] for i in range(0,len(names),2)]
    await update.message.reply_text("📶 Select Operator:",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True))
    return OPERATOR

async def operator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["operator"]=update.message.text
    await update.message.reply_text("💰 Enter Amount:", reply_markup=ReplyKeyboardRemove())
    return AMOUNT

async def amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    amount_val=update.message.text
    mobile_num=context.user_data.get("mobile")
    op_name=context.user_data.get("operator")
    sp_key=OPERATORS.get(op_name)
    if not sp_key:
        await update.message.reply_text("❌ Invalid Operator.")
        return ConversationHandler.END
    params={"UserID":USER_ID,"Token":API_TOKEN,"Account":mobile_num,"Amount":amount_val,
            "SPKey":sp_key,"APIRequestID":str(uuid.uuid4()),"GEOCode":GEO_CODE,
            "CustomerNumber":mobile_num,"Pincode":PINCODE,"Format":"1"}
    try:
        data=requests.get(API_URL,params=params,timeout=30).json()
        if str(data.get("STATUS"))=="2":
            await update.message.reply_text(f"✅ Success\nMobile:{mobile_num}\nAmount:₹{amount_val}")
        else:
            await update.message.reply_text(f"❌ Failed: {data.get('MSG')}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

if __name__ == "__main__":
    app=ApplicationBuilder().token(BOT_TOKEN).build()
    conv=ConversationHandler(
        entry_points=[CommandHandler("recharge", recharge)],
        states={
            MOBILE:[MessageHandler(filters.TEXT & ~filters.COMMAND, mobile)],
            OPERATOR:[MessageHandler(filters.TEXT & ~filters.COMMAND, operator)],
            AMOUNT:[MessageHandler(filters.TEXT & ~filters.COMMAND, amount)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    app.run_polling(drop_pending_updates=True)
