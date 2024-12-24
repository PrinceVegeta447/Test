from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
import random

# Define initial battle stats
def create_battle_ui(player_hp, enemy_hp, enemy_name):
    battle_message = (
        f"⚔️ You are battling *{enemy_name}*! ⚔️\n\n"
        f"🛡️ *Your Stats:*\n"
        f"Health: {player_hp}\n\n"
        f"💥 *Enemy Stats:*\n"
        f"Health: {enemy_hp}\n"
        "Attack: 15\n\n"
        "Choose your action wisely!"
    )
    # Battle action buttons
    keyboard = [
        [
            InlineKeyboardButton("👊 Attack", callback_data="attack"),
            InlineKeyboardButton("🏃‍♂️ Flee", callback_data="flee"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return battle_message, reply_markup


# Process the battle actions
async def process_battle_action(action, player_data, enemy_data):
    if action == "attack":
        # Player attacks
        player_attack = random.randint(10, 20)
        enemy_data["health"] -= player_attack

        if enemy_data["health"] <= 0:
            return (
                f"🎉 You attacked and defeated *{enemy_data['name']}*! 🎉\n"
                "Congratulations on your victory! 🏆"
            )

        # Enemy's turn to attack
        enemy_attack = random.randint(5, 15)
        player_data["health"] -= enemy_attack

        if player_data["health"] <= 0:
            return (
                f"💀 You attacked *{enemy_data['name']}* but were defeated. 💀\n"
                "Better luck next time! 🍀"
            )

        return (
            f"👊 You attacked *{enemy_data['name']}* and dealt {player_attack} damage.\n"
            f"🩸 *Enemy Health:* {enemy_data['health']}\n\n"
            f"⚠️ *{enemy_data['name']}* counterattacked and dealt {enemy_attack} damage.\n"
            f"🩸 *Your Health:* {player_data['health']}\n"
            "Choose your next action!"
        )

    elif action == "flee":
        flee_success = random.choice([True, False])
        if flee_success:
            return "🏃‍♂️ You managed to escape! 💨"
        else:
            return "❌ You failed to flee, and the battle continues! 😓"

    return "❓ Invalid action."  # Default case for unexpected action


# Define callback for handling the battle actions
async def handle_battle_action(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()  # Acknowledge the button press

    # Fetch player and enemy data from context
    player_data = context.user_data.get("player_data", {"health": 100, "name": "Player"})
    enemy_data = context.user_data.get("enemy_data", {"health": 100, "name": "Enemy"})

    action = query.data  # Extract action from the button's callback data

    # Check if action is valid and execute
    if action not in ["attack", "flee"]:
        await query.edit_message_text("❓ Invalid selection! Please choose a valid action.", parse_mode="Markdown")
        return

    battle_result = await process_battle_action(action, player_data, enemy_data)

    # Update the battle message with the result of the action
    await query.edit_message_text(battle_result, parse_mode="Markdown")

    # Update context with the latest player and enemy data
    context.user_data["player_data"] = player_data
    context.user_data["enemy_data"] = enemy_data

    # After processing action, recreate the battle UI for new possible actions
    updated_battle_message, updated_reply_markup = create_battle_ui(
        player_data["health"], enemy_data["health"], enemy_data["name"]
    )

    # Edit the message with the new battle status and action buttons
    await query.edit_message_text(updated_battle_message, parse_mode="Markdown", reply_markup=updated_reply_markup)
