from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Load Config
import json
with open("config.json", "r") as file:
    config = json.load(file)

TOKEN = config["bot_token"]

# Start Command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the Dragon Ball Z Game Bot! Type /play to start.")

# Main Function
def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Command Handlers
    dispatcher.add_handler(CommandHandler("start", start))

    # Start Bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
