from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackContext
import random  # Import inventory functions

# Define the developer's Telegram user ID (replace with your actual ID)
DEVELOPER_ID = 123456789  # Your developer Telegram ID

# Example items and enemies
items = ["Zeni 💰", "Senzu Bean 🍚"]
enemies = ["Frieza 👑", "Cell 🟢", "Majin Buu 🍬"]

# Explore function with inventory logic
async def explore(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    # Randomly decide what happens during exploration
    event_type = random.choice(["item", "enemy", "nothing"])

    # 1 in 5000 chance of finding Dragon Ball
    if random.randint(1, 5000) == 300:
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

# View Inventory Command
async def inventory(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_inv = get_inventory(user_id)
    if not user_inv:
        await update.message.reply_text("Your inventory is empty! Start exploring to find items! 🍀")
    else:
        inventory_items = "\n".join([f"{item}: {count}" for item, count in user_inv.items()])  # Display item and its count
        await update.message.reply_text(f"Your inventory:\n{inventory_items}")

# Add Item Command (Developer Only)
async def add_item_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id != DEVELOPER_ID:
        await update.message.reply_text("❌ You don't have permission to use this command!")
        return

    # Example to add an item to the developer's inventory
    item = "Zeni 💰"  # Example item
    add_item(user_id, item)
    await update.message.reply_text(f"✅ Item '{item}' added to your inventory!")

# Clear Inventory Command (Developer Only)
async def clear_inventory_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id != DEVELOPER_ID:
        await update.message.reply_text("❌ You don't have permission to use this command!")
        return

    # Clear the developer's inventory
    clear_inventory(user_id)
    await update.message.reply_text("✅ Your inventory has been cleared!")
