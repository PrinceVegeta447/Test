from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Global dictionary to track player states (simplified, can be replaced with database)
player_state = {}

# Handle /play command
async def play(update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Check if the user has already started their journey
    if user_id in player_state and player_state[user_id]["started"]:
        await update.message.reply_text("You have already started your journey!")
        return

    # If not started, initialize the player's state
    player_state[user_id] = {"started": True, "character": None}

    # Create the inline keyboard for character selection
    keyboard = [
        [
            InlineKeyboardButton("Goku", callback_data='goku'),
            InlineKeyboardButton("Vegeta", callback_data='vegeta')
        ],
        [
            InlineKeyboardButton("Frieza", callback_data='frieza'),
            InlineKeyboardButton("Piccolo", callback_data='piccolo')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message to the user
    await update.message.reply_text(
        "Welcome to your Dragon Ball Z adventure! Choose your character:",
        reply_markup=reply_markup
    )

# Handle character selection callback
async def character_callback(update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.from_user.id
    character = update.callback_query.data

    # Update the player's selected character
    if user_id in player_state:
        player_state[user_id]["character"] = character

    # Respond with a confirmation message
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        f"You have selected {character}. Your journey begins now!"
    )
