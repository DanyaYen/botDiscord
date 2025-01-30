import json
import discord
from datetime import datetime, timezone

def create_embed(title, description, color=discord.Color.blue()):
    """Creates an embed message with current UTC timestamp"""
    return discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.now(timezone.utc)  # Правильный способ получения UTC времени
    )
def load_json(filename):
    """Loads data from JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_json(filename, data):
    """Saves data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)