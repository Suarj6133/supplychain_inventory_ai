from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# 🔑 Replace this with your BotFather token
TELEGRAM_TOKEN = "8370047565:AAF_d-_Njg7HBcfLyUgrEz-YtHpfoUPSbGQ"

# URL of your Flask API endpoint
FLASK_API_URL = "http://127.0.0.1:5000/api/query"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I’m your Grocery Assistant.\n"
        "Ask me a question about your grocery data, and I’ll fetch answers."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    try:
        # Send query to Flask API
        response = requests.post(FLASK_API_URL, json={"query": user_message})
        
        if response.status_code == 200:
            answer = response.json().get("answer", "⚠️ No answer received.")
        else:
            answer = f"❌ Error: Flask API returned {response.status_code}"
    
    except Exception as e:
        answer = f"❌ Could not connect to backend: {e}"
    
    await update.message.reply_text(answer)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Telegram bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
