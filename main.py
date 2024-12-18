import json
import os
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import Update
from play import play, character_callback
import logging

# Load Config
with open("config.json", "r") as file:
    config = json.load(file)

TOKEN = config["bot_token"]
WEBHOOK_URL = config["webhook_url"]  # Correctly access the webhook URL

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Start Command
async def start(update, context):
    await update.message.reply_text("Welcome to the Dragon Ball Z Game Bot! Type /play to start.")

# Main Function
def main():
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("play", play))
    application.add_handler(CallbackQueryHandler(character_callback))

    # Set webhook (using HTTPS URL from config)
    application.bot.set_webhook(WEBHOOK_URL)

    # Get the port from the environment or default to 5000
    port = int(os.environ.get("PORT", 5000))

    # Run the bot with webhook
    application.run_webhook(listen="0.0.0.0", port=port, url_path=TOKEN)

if __name__ == "__main__":
    main()
