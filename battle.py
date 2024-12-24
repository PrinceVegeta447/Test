from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
import random

# Battle variables (for simplicity, we will store them in a dictionary)
battles = {}

# Function to start a battle
async def battle(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data.split('_')

    # Extract battle info from the callback data
    action = data[0]
    enemy = data[1]
    
    if action == "battle":
        # Initialize battle status
        battles[user_id] = {
            "enemy": enemy,
            "user_health": 100,
            "enemy_health": 100,
            "user_attack": 20,
            "enemy_attack": 15
        }

        # Update the message to show battle UI
        battle_message = f"⚔️ Battle Started! ⚔️\n\nYou are fighting *{enemy}*!\n\nYour Health: 100\n{enemy}'s Health: 100\n\nWhat will you do next?"
        keyboard = [
            [InlineKeyboardButton("🔨 Attack", callback_data=f"attack_{user_id}")],
            [InlineKeyboardButton("🛡️ Defend", callback_data=f"defend_{user_id}")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(battle_message, reply_markup=reply_markup)


# Function to handle attack action
async def attack(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    if user_id in battles:
        battle = battles[user_id]

        # Calculate the damage dealt
        damage_to_enemy = battle["user_attack"]
        damage_to_user = battle["enemy_attack"]

        # Update the health values
        battle["enemy_health"] -= damage_to_enemy
        battle["user_health"] -= damage_to_user

        # Check if the battle is over
        if battle["enemy_health"] <= 0:
            await query.edit_message_text(f"You defeated *{battle['enemy']}*! 🏆\n\nYour Health: {battle['user_health']}")
            del battles[user_id]  # End the battle
        elif battle["user_health"] <= 0:
            await query.edit_message_text(f"You were defeated by *{battle['enemy']}* 😞\n\nYour Health: 0")
            del battles[user_id]  # End the battle
        else:
            battle_message = f"⚔️ Battle Update ⚔️\n\nYou attacked *{battle['enemy']}*! 💥\n\nYour Health: {battle['user_health']}\n{battle['enemy']}'s Health: {battle['enemy_health']}\n\nWhat will you do next?"
            keyboard = [
                [InlineKeyboardButton("🔨 Attack", callback_data=f"attack_{user_id}")],
                [InlineKeyboardButton("🛡️ Defend", callback_data=f"defend_{user_id}")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(battle_message, reply_markup=reply_markup)


# Function to handle defend action
async def defend(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    if user_id in battles:
        battle = battles[user_id]

        # Calculate the damage (less damage for defend)
        damage_to_enemy = battle["user_attack"] // 2
        damage_to_user = battle["enemy_attack"] // 2

        # Update health after defend action
        battle["enemy_health"] -= damage_to_enemy
        battle["user_health"] -= damage_to_user

        # Check if the battle is over
        if battle["enemy_health"] <= 0:
            await query.edit_message_text(f"You defeated *{battle['enemy']}*! 🏆\n\nYour Health: {battle['user_health']}")
            del battles[user_id]  # End the battle
        elif battle["user_health"] <= 0:
            await query.edit_message_text(f"You were defeated by *{battle['enemy']}* 😞\n\nYour Health: 0")
            del battles[user_id]  # End the battle
        else:
            battle_message = f"⚔️ Battle Update ⚔️\n\nYou defended yourself from *{battle['enemy']}*'s attack! 🛡️\n\nYour Health: {battle['user_health']}\n{battle['enemy']}'s Health: {battle['enemy_health']}\n\nWhat will you do next?"
            keyboard = [
                [InlineKeyboardButton("🔨 Attack", callback_data=f"attack_{user_id}")],
                [InlineKeyboardButton("🛡️ Defend", callback_data=f"defend_{user_id}")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(battle_message, reply_markup=reply_markup)
