from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler
import random

# Example items and enemies
items = ["Dragon Ball", "Zeni", "Senzu Bean"]
enemies = ["Frieza", "Cell", "Majin Buu"]

# Battle function
async def battle(update: Update, context: CallbackContext, enemy: str):
    # Simulate a simple battle outcome
    user_health = 100
    enemy_health = 100
    while user_health > 0 and enemy_health > 0:
        # Simulate a turn in the battle
        user_attack = random.randint(10, 20)
        enemy_attack = random.randint(5, 15)
        
        enemy_health -= user_attack
        user_health -= enemy_attack
        
        # Send updates about the battle
        await update.message.reply_text(f"You attacked {enemy} for {user_attack} damage! {enemy} has {enemy_health} HP left.")
        await update.message.reply_text(f"{enemy} attacked you for {enemy_attack} damage! You have {user_health} HP left.")
        
        if user_health <= 0:
            await update.message.reply_text("You lost the battle! Try again.")
            return
        elif enemy_health <= 0:
            await update.message.reply_text(f"You defeated {enemy}! Congratulations!")
            return

# Handle the battle button press
async def battle_button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()  # Acknowledge the button press
    
    # Get the enemy name from the callback data
    enemy = query.data
    print(f"Battle initiated with: {enemy}")  # Debugging line to check the enemy name

    # Start the battle
    await battle(update, context, enemy)

# Explore function
async def explore(update: Update, context: CallbackContext):
    # Randomly decide what happens during exploration
    event_type = random.choice(["item", "enemy", "nothing"])
    
    if event_type == "item":
        item_found = random.choice(items)
        await update.message.reply_text(f"You found a {item_found}!")
    elif event_type == "enemy":
        enemy_encountered = random.choice(enemies)
        
        # Create an inline button for battle
        keyboard = [
            [InlineKeyboardButton("Battle", callback_data=enemy_encountered)]  # Use the enemy's name as callback data
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(f"You encountered {enemy_encountered}! Prepare to fight!", reply_markup=reply_markup)
    else:
        await update.message.reply_text("You explored the area but found nothing. Keep searching!")
