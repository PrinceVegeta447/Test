from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
import random

# Example items and enemies
items = ["Dragon Ball", "Zeni", "Senzu Bean"]
enemies = ["Frieza", "Cell", "Majin Buu"]

# Define the explore function
async def explore(update: Update, context: CallbackContext):
    # Randomly decide what happens during exploration
    event_type = random.choice(["item", "enemy", "nothing"])
    
    if event_type == "item":
        item_found = random.choice(items)
        await update.message.reply_text(f"You found a {item_found}!")
    elif event_type == "enemy":
        enemy_encountered = random.choice(enemies)
        await update.message.reply_text(f"You encountered {enemy_encountered}! Prepare to fight!")
    else:
        await update.message.reply_text("You explored the area but found nothing. Keep searching!")
