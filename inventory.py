# inventory.py
user_inventory = {}

def initialize_inventory(user_id):
    """Ensure the user has an inventory."""
    if user_id not in user_inventory:
        user_inventory[user_id] = {}

def add_item(user_id, item):
    """Add an item to the user's inventory and increase its count."""
    initialize_inventory(user_id)
    if item in user_inventory[user_id]:
        user_inventory[user_id][item] += 1
    else:
        user_inventory[user_id][item] = 1

def get_inventory(user_id):
    """Get the user's inventory."""
    initialize_inventory(user_id)
    return user_inventory[user_id]

def clear_inventory(user_id):
    """Clear the user's inventory (for testing purposes)."""
    user_inventory[user_id] = {}
