from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
import random
from inventory import add_item, get_inventory

# Example items and enemies
items = ["Zeni 💰", "Senzu Bean 🍚"]
enemies = ["Frieza 👑", "Cell 🟢", "Majin Buu 🍬"]

# A simple structure for player stats
player_stats = {
    "hp": 100,  # Player health points
    "damage": 20,  # Player attack damage
    "defense": 10,  # Player defense points
}

# A simple structure for enemy stats
enemy_stats = {
    "Frieza 👑": {"hp": 150, "damage": 25, "defense": 5},
    "Cell 🟢": {"hp": 120, "damage": 30, "defense": 10},
    "Majin Buu 🍬": {"hp": 100, "damage": 20, "defense": 15},
}

# Exploration function with both item and battle logic
async def explore(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
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
        
        # Create an inline button for battle
        keyboard = [
            [InlineKeyboardButton(f"💥 Battle {enemy_encountered}", callback_data=f"battle_{enemy_encountered}")]
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

# Battle function triggered by the "Battle" button press
async def battle(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    # Extract enemy name from callback data
    enemy = query.data.split('_')[1]
    enemy_data = enemy_stats[enemy]

    # Get player stats (you can implement this to get stats from a database or in-memory storage)
    player_data = player_stats

    # Present battle options: Attack, Defend, or Run
    keyboard = [
        [InlineKeyboardButton("💥 Attack", callback_data="attack")],
        [InlineKeyboardButton("🛡️ Defend", callback_data="defend")],
        [InlineKeyboardButton("🏃‍♂️ Run", callback_data="run")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send initial battle message
    await query.edit_message_text(
        f"You are now facing *{enemy}*! Choose your next move:",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

    # Process battle logic based on user action (e.g., attack, defend)
    async def process_battle_action(action: str, player_data, enemy_data):
        if action == "attack":
            # Player attacks enemy
            damage_dealt = max(0, player_data["damage"] - enemy_data["defense"])
            enemy_data["hp"] -= damage_dealt
            battle_result = f"You dealt {damage_dealt} damage to {enemy}. 🥊"

            if enemy_data["hp"] <= 0:
                battle_result += "\nYou have defeated the enemy! 🎉"
            else:
                # Enemy counterattacks
                enemy_damage = max(0, enemy_data["damage"] - player_data["defense"])
                player_data["hp"] -= enemy_damage
                battle_result += f"\n{enemy} attacked and dealt {enemy_damage} damage to you! 💥"

                if player_data["hp"] <= 0:
                    battle_result += "\nYou were defeated... 😢"

            return battle_result

        elif action == "defend":
            # Player defends (reduce incoming damage)
            battle_result = "You brace yourself and reduce the incoming damage! 🛡️"

            return battle_result

        elif action == "run":
            # Player tries to flee (50% chance of success)
            flee_success = random.choice([True, False])
            if flee_success:
                battle_result = "You managed to escape! 🏃‍♂️💨"
            else:
                battle_result = "You failed to run away and the battle continues! 😓"

            return battle_result

        return "Invalid action."

    # Define callback for handling the battle actions
    async def handle_battle_action(update: Update, context: CallbackContext):
        query = update.callback_query
        await query.answer()

        action = query.data
        battle_result = await process_battle_action(action, player_data, enemy_data)

        # Update the battle message with the result of the action
        await query.edit_message_text(battle_result, parse_mode="Markdown")

    # Add handler for battle actions (Attack, Defend, Run)
    application.add_handler(CallbackQueryHandler(handle_battle_action, pattern=r"^(attack|defend|run)$"))
