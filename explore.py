from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
import random
from inventory import add_item, get_inventory
from battle import create_battle_ui
# Example items and enemies
items = ["Zeni 💰", "Senzu Bean 🍚"]
enemies = ["Frieza 👑", "Cell 🟢", "Majin Buu 🍬"]

# Explore function
async def explore(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    # Randomly decide what happens during exploration
    event_type = random.choice(["item", "enemy", "nothing"])

    # 1 in 5000 chance of finding Dragon Ball
    if random.randint(1, 5000) == 1:
        item_found = "Dragon Ball 🟡"
        add_item(user_id, item_found)  # Add Dragon Ball to inventory
        await update.message.reply_text(
            f"✨ Congratulations! You found a *{item_found}* during your exploration! ✨\n\n"
            "What a rare and amazing find! Keep exploring to find more treasures! 😎",
            parse_mode="Markdown"
        )
    elif event_type == "item":
        item_found = random.choice(items)
        add_item(user_id, item_found)  # Add the found item to inventory
        await update.message.reply_text(
            f"✨ You found a *{item_found}* during your exploration! ✨\n\n"
            "What a lucky find! Keep exploring to find more treasures! 😎",
            parse_mode="Markdown"
        )
    elif event_type == "enemy":
        enemy_encountered = random.choice(enemies)

        # Store enemy data in user context
        enemy_data = {"name": enemy_encountered, "health": 100, "attack": 15}
        context.user_data["enemy_data"] = enemy_data

        # Initialize player data
        context.user_data["player_data"] = {"health": 100}   

 if event_type == "enemy":
    enemy_encountered = random.choice(list(enemies.keys()))
    player_hp = 100
    enemy_hp = enemies[enemy_encountered]["HP"]

    # Generate battle UI using create_battle_ui from battle.py
    battle_message, reply_markup = create_battle_ui(player_hp, enemy_hp)

    await update.message.reply_text(
        battle_message,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

        # Create an inline button for battle
        keyboard = [
            [InlineKeyboardButton(f"💥 Battle {enemy_encountered}", callback_data="start_battle")]  # Button text with emoji
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


# Command to view inventory
async def inventory(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_inv = get_inventory(user_id)  # Get the user's inventory

    if user_inv:
        items_str = "\n".join([f"{item}: {count}" for item, count in user_inv.items()])
        await update.message.reply_text(
            f"🧳 *Your Inventory:*\n\n{items_str}",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "🧳 Your inventory is empty. Keep exploring to find items! 🍀",
            parse_mode="Markdown"
        )
