from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from play import play, character_callback
# Load Config
import json
with open("config.json", "r") as file:
    config = json.load(file)

TOKEN = config["bot_token"]

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Dragon Ball Z Game Bot! Type /play to start.")

# Main Function
def main():
    # Create the application
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
