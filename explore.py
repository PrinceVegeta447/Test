from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackContext
import random

# Example items with emojis
items = ["Zeni 💰", "Senzu Bean 🍚"]
enemies = ["Frieza 👑", "Cell 🟢", "Majin Buu 🍬"]

# Explore function with a 1 in 5000 chance for Dragon Ball
async def explore(update: Update, context: CallbackContext):
    # Randomly decide what happens during exploration
    event_type = random.choice(["item", "enemy", "nothing"])

    # 1 in 5000 chance of finding Dragon Ball
    if random.randint(1, 5000) == 1:
        item_found = "Dragon Ball 🟡"
        await update.message.reply_text(
            f"✨ Congratulations! You found a *{item_found}* during your exploration! ✨\n\n"
            "What a rare and amazing find! Keep exploring to find more treasures! 😎",
            parse_mode="Markdown"
        )
    elif event_type == "item":
        item_found = random.choice(items)
        await update.message.reply_text(
            f"✨ You found a *{item_found}* during your exploration! ✨\n\n"
            "What a lucky find! Keep exploring to find more treasures! 😎",
            parse_mode="Markdown"
        )
    elif event_type == "enemy":
        enemy_encountered = random.choice(enemies)
        
        # Create an inline button for battle
        keyboard = [
            [InlineKeyboardButton(f"💥 Battle {enemy_encountered}", callback_data=enemy_encountered)]  # Button text with emoji
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"⚠️ Oh no! You've encountered *{enemy_encountered}*! ⚠️\n"
            "Prepare yourself for battle! 💪",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            "🔍 You explored the area but found nothing this time. Better luck next time! 🍀",
            parse_mode="Markdown"
        )

# Handler for the explore command
def start_exploration(application):
    # Register the explore command handler
    application.add_handler(CommandHandler("explore", explore))
