import os

# Fetch API ID and ensure it has a default value
API_ID = int(os.environ.get("API_ID", "28094744"))  # Replace 12345 with your default

# Fetch API_HASH with a default empty string
API_HASH = os.environ.get("API_HASH", "a75af4285edc7747c57bb19147ca0b9b")

# Fetch BOT_TOKEN with a default empty string
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7982396596:AAGZJZj1Gqc6XV46-9nXl-af1mhwAnLV6PU")
