from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Global dictionary to track player states
player_state = {}

# Load characters from JSON
import json
with open("game_data.json", "r") as file:
    characters = json.load(file)

async def play(update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id in player_state and player_state[user_id]["started"]:
        await update.message.reply_text("You have already started your journey!")
        return

    player_state[user_id] = {"started": True, "character": None}

    # Create inline keyboard for character selection
    keyboard = [
        [InlineKeyboardButton("Goku", callback_data="goku"),
         InlineKeyboardButton("Vegeta", callback_data="vegeta")],
        [InlineKeyboardButton("Frieza", callback_data="frieza"),
         InlineKeyboardButton("Piccolo", callback_data="piccolo")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Welcome to your Dragon Ball Z adventure! Choose your character:",
        reply_markup=reply_markup
    )

async def character_callback(update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    selected_character = query.data  # Get the callback data (e.g., "goku")

    # Ensure the callback data is valid
    if selected_character not in characters:
        await query.answer("Invalid selection. Please try again.")
        return

    if user_id in player_state:
        player_state[user_id]["character"] = selected_character

    await query.answer()
    await query.edit_message_text(
        f"You have selected {characters[selected_character]['name']}. Your journey begins now!"
    )
