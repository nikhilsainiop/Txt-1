import os

# Fetch API ID and ensure it has a default value
API_ID = int(os.environ.get("API_ID", "28094744"))  # Replace 12345 with your default

# Fetch API_HASH with a default empty string
API_HASH = os.environ.get("API_HASH", "a75af4285edc7747c57bb19147ca0b9b")

# Fetch BOT_TOKEN with a default empty string
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7982396596:AAGZJZj1Gqc6XV46-9nXl-af1mhwAnLV6PU")

# Define LOG variable properly
LOG = True  # Set to False if logging is not required

# Uncomment or define UPDATE_GRP if needed
# UPDATE_GRP = "your_group_id"

# Uncomment or define auth_chats if needed
# auth_chats = []

# Admins list
try:
    ADMINS = []
    for x in (os.environ.get("ADMINS", "1928404158").split()):  # Default admin: 502980590
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")
ADMINS.append(OWNER)



