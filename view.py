import json
from telegram import Update
from telegram.ext import ContextTypes
from play import player_state

# Load characters from JSON file
with open("game_data.json", "r") as file:
    characters = json.load(file)

# Handle /view_character command
async def viewch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Check if the user has selected a character
    if user_id not in player_state or player_state[user_id]["character"] is None:
        await update.message.reply_text("You haven't selected a character yet. Use /play to start your journey!")
        return

    # Get the character info
    selected_character = player_state[user_id]["character"].lower()
    character_info = characters.get(selected_character)

    if not character_info:
        await update.message.reply_text("Error: Character data not found.")
        return

    # Prepare character details as a message
    character_details = (
        f"👤 **Character**: {character_info['name']}\n"
        f"💥 **Power**: {character_info['power']}\n"
        f"💪 **Strength**: {character_info['strength']}\n"
        f"✨ **Skills**: {', '.join(character_info['skills'])}\n"
        f"📖 **Bio**: {character_info['bio']}"
    )

    # Send character details as a message
    await update.message.reply_text(character_details, parse_mode="Markdown")
