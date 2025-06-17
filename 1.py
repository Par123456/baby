import json
import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

BOT_TOKEN = "7658073484:AAFlGTDzC7VQYg1bt5mNonTOBiuRXs8Jjqw"
MOM_ID = 2065070882
DAD_ID = 6508600903
MEMORY_FILE = "memory.json"
BABY_NAME = "کوروش"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def baby_talk(text):
    endings = [" مامان", " بابا", " 🍼", " 😇", " دوستت دارم", " کوچولو", " 😅"]
    return text + random.choice(endings)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text:
        return

    chat_type = update.effective_chat.type
    if chat_type not in ['group', 'supergroup']:
        return

    user_id = msg.from_user.id
    text = msg.text.strip()
    lowered = text.lower()
    memory = load_memory()

    if user_id in [MOM_ID, DAD_ID] and text.startswith("یاد بگیر"):
        parts = text[len("یاد بگیر"):].strip().split("=>")
        if len(parts) != 2:
            await msg.reply_text("بگو: یاد بگیر جمله => جواب")
            return
        key = parts[0].strip().lower()
        value = parts[1].strip()
        memory[key] = value
        save_memory(memory)
        await msg.reply_text("چشم یاد گرفتم 😇")
        return

    if user_id in [MOM_ID, DAD_ID] and "فراموش کن" in lowered:
        save_memory({})
        await msg.reply_text("یادم رفت همه چیز 😭")
        return

    if user_id in [MOM_ID, DAD_ID] and "چی یاد گرفتی" in lowered:
        if memory:
            text = "\n".join([f"• {k} => {v}" for k, v in list(memory.items())[-10:]])
            await msg.reply_text(f"یاد گرفتم اینا رو:\n{text}")
        else:
            await msg.reply_text("من هیچی بلد نیستم هنوز 🥺")
        return

    if user_id not in [MOM_ID, DAD_ID] and BABY_NAME.lower() not in lowered:
        return

    for key in memory:
        if key in lowered:
            await msg.reply_text(baby_talk(memory[key]))
            return

    await msg.reply_text("بلد نیستم 😭 بگو یاد بگیر جمله => جواب")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("🤖 ربات کودک فعال شد...")
    app.run_polling()
