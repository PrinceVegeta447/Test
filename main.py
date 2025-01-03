import json
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from play import play, character_callback
from view import viewch
from explore import explore, inventory
from inventory import add_item, get_inventory
from battle import create_battle_ui, handle_battle_action
import logging

# Load Config
with open("config.json", "r") as file:
    config = json.load(file)

TOKEN = config["bot_token"]



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Start Command
async def start(update, context):
    await update.message.reply_text("Welcome to the Dragon Ball Z Game Bot! Type /play to start.")

# Main Function
def main():
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add handlers for different commands and callbacks
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("play", play))
    application.add_handler(CommandHandler("viewch", viewch))  # Add the view_character handler
    application.add_handler(CallbackQueryHandler(character_callback))
    application.add_handler(CommandHandler("explore", explore))
    application.add_handler(CommandHandler("inventory", inventory)) # Trigger battle when enemy encountered
    application.add_handler(CallbackQueryHandler(handle_battle_action, pattern=r"^(attack|defend|run)$"))  # Battle action handlers
    
    # Start polling
    application.run_polling()

if __name__ == "__main__":
    main()
