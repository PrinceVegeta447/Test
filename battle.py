from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
import random

# Example enemies and battle states
enemies = {
    "Frieza 👑": {"hp": 100, "attack": 30},
    "Cell 🟢": {"hp": 120, "attack": 35},
    "Majin Buu 🍬": {"hp": 150, "attack": 25}
}

# Battle state to track user health and progress
user_battle_state = {}

# Start the battle when the user clicks the battle button
async def battle(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    enemy_name = update.callback_query.data  # Extract enemy name from callback data
    enemy = enemies.get(enemy_name)

    if not enemy:
        await update.callback_query.answer("Invalid enemy encountered!")
        return

    # Initialize user battle state if it doesn't exist
    if user_id not in user_battle_state:
        user_battle_state[user_id] = {
            "hp": 100,  # User starts with 100 HP
            "enemy": enemy_name,
            "enemy_hp": enemy["hp"]
        }

    # Create inline buttons for battle actions
    keyboard = [
        [InlineKeyboardButton("💥 Attack", callback_data="attack"),
         InlineKeyboardButton("🛡️ Defend", callback_data="defend"),
         InlineKeyboardButton("🏃‍♂️ Run", callback_data="run")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the battle intro message
    await update.callback_query.answer()
    await update.callback_query.message.edit_text(
        f"⚔️ Battle started against *{enemy_name}*! ⚔️\n\n"
        f"Your HP: 100\n{enemy_name}'s HP: {enemy['hp']}\n\n"
        "Choose an action to begin the fight!",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# Handle user actions in battle (attack, defend, run)
async def handle_battle_action(update: Update, context: CallbackContext):
    user_id = update.callback_query.from_user.id
    action = update.callback_query.data
    battle_state = user_battle_state.get(user_id)

    if not battle_state:
        await update.callback_query.answer("No active battle found!")
        return

    enemy_name = battle_state["enemy"]
    enemy = enemies.get(enemy_name)
    user_hp = battle_state["hp"]
    enemy_hp = battle_state["enemy_hp"]

    if action == "attack":
        damage = random.randint(20, 40)  # Random attack damage
        enemy_hp -= damage
        battle_state["enemy_hp"] = max(0, enemy_hp)

        # Enemy counterattack
        enemy_damage = random.randint(10, enemy["attack"])
        user_hp -= enemy_damage
        battle_state["hp"] = max(0, user_hp)

        battle_result = f"You dealt *{damage}* damage to {enemy_name}. 💥\n" \
                        f"{enemy_name} dealt *{enemy_damage}* damage to you. 🥊\n"
    elif action == "defend":
        defense = random.randint(5, 20)  # Random defense value
        enemy_damage = max(0, random.randint(10, enemy["attack"]) - defense)
        user_hp -= enemy_damage
        battle_state["hp"] = max(0, user_hp)

        battle_result = f"You defended successfully and reduced damage to *{enemy_damage}*.\n"
    elif action == "run":
        battle_result = f"You ran away from the battle! 🏃‍♂️💨"
        del user_battle_state[user_id]  # End the battle when running away
    else:
        battle_result = "Invalid action! Try again."

    # Update the battle status message
    await update.callback_query.answer()
    
    # Check if the battle is over
    if battle_state["hp"] <= 0:
        battle_result += f"\nYou were defeated by *{enemy_name}*! 😢"
        del user_battle_state[user_id]  # End the battle after defeat
    elif battle_state["enemy_hp"] <= 0:
        battle_result += f"\nYou defeated *{enemy_name}*! 🎉"
        del user_battle_state[user_id]  # End the battle after victory

    # Send updated battle status
    keyboard = [
        [InlineKeyboardButton("💥 Attack", callback_data="attack"),
         InlineKeyboardButton("🛡️ Defend", callback_data="defend"),
         InlineKeyboardButton("🏃‍♂️ Run", callback_data="run")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Update battle message with results
    await update.callback_query.message.edit_text(
        f"⚔️ Battle against *{enemy_name}* ⚔️\n\n"
        f"Your HP: {battle_state['hp']}\n{enemy_name}'s HP: {battle_state['enemy_hp']}\n\n"
        f"{battle_result}",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
