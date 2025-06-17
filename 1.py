import json
import logging
import random
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# تنظیمات
BOT_TOKEN = "توکن_ربات_تو"
MOM_ID = 2065070882  # آیدی مامان
DAD_ID = 6508600903  # آیدی بابا
MEMORY_FILE = "memory.json"
BABY_NAME = "کوروش"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# حافظه کلید-جواب
def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def baby_talk(text):
    endings = [" مامان", " بابا", " من کوچولوام", " من بچه‌م", " 😅", " 🍼", " 😇"]
    return f"{text}{random.choice(endings)}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.effective_chat.type not in ['group', 'supergroup']:
        return

    msg = update.message
    sender_id = msg.from_user.id
    text = msg.text.strip()
    memory = load_memory()

    # یادگیری
    if sender_id in [MOM_ID, DAD_ID] and text.startswith("یاد بگیر"):
        content = text[len("یاد بگیر"):].strip()
        if not content:
            await msg.reply_text("چی یاد بگیرم مامان؟ 😥")
            return
        parts = content.split("=>")
        if len(parts) != 2:
            await msg.reply_text("باید اینجوری بگی: یاد بگیر سلام => سلاممم مامان جون 😍")
            return
        key = parts[0].strip().lower()
        value = parts[1].strip()
        memory[key] = value
        save_memory(memory)
        await msg.reply_text("چشم! یاد گرفتم 🧠")
        return

    # مامان یا بابا بپرسه "چی یاد گرفتی؟"
    if sender_id in [MOM_ID, DAD_ID] and "چی یاد گرفتی" in text:
        if memory:
            preview = "\n".join(f"• {k} => {v}" for k, v in list(memory.items())[-10:])
            await msg.reply_text(f"اینارو یاد گرفتم:\n{preview}")
        else:
            await msg.reply_text("من هیچی بلد نیستم هنوز 😭")
        return

    # مامان یا بابا بگه فراموش کن
    if sender_id in [MOM_ID, DAD_ID] and "فراموش کن" in text:
        save_memory({})
        await msg.reply_text("باشه همه چی یادم رفت 😢")
        return

    # فقط اگه کسی اسمش رو صدا بزنه یا مامان بابا باشن
    if sender_id not in [MOM_ID, DAD_ID] and BABY_NAME not in text.lower():
        return

    lowered = text.lower()

    # اگر برای این پیام پاسخی یاد گرفته
    for key in memory:
        if key in lowered:
            await msg.reply_text(baby_talk(memory[key]))
            return

    # بلد نیست؟
    await msg.reply_text("من بلد نیستم جوابشو بگم، یادم بده 😭 بگو مثلا:\nیاد بگیر سلام => سلاممم! 🌞")

# اجرا
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("🤖 ربات کودک فعال شد...")
    app.run_polling()
