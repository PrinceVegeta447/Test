from telegram import Update
from telegram.ext import ContextTypes
from play import characters, player_state  # Import the player state and character data

# Handle /view_character command
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Check if the user has selected a character
    if user_id not in player_state or player_state[user_id]["character"] is None:
        await update.message.reply_text("You haven't selected a character yet. Use /play to start your journey!")
        return

    # Get the character info
    selected_character = player_state[user_id]["character"]
    character_info = characters[selected_character]

    # Send the character details to the player
    character_details = (
        f"Character: {character_info['name']}\n"
        f"Power: {character_info['power']}\n"
        f"Strength: {character_info['strength']}"
    )

    await update.message.reply_text(character_details)
