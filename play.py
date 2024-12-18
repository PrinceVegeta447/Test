import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, ContextTypes

# Load game data
with open("game_data.json", "r") as file:
    game_data = json.load(file)

# Global variable to track player choices
player_choices = {}

# Play command: Show inline buttons for character selection
async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    characters = list(game_data["characters"].keys())
    keyboard = [
        [InlineKeyboardButton(char, callback_data=char)] for char in characters
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Choose your character:", reply_markup=reply_markup
    )

# Handle inline button selection
async def character_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    selected_character = query.data

    if selected_character in game_data["characters"]:
        player_choices[user_id] = selected_character
        await query.edit_message_text(
            f"You chose {selected_character}! Type /battle to begin."
        )
    else:
        await query.edit_message_text("Invalid choice. Please use /play to select again.")
