import os

# Fetch API ID and ensure it has a default value
API_ID = int(os.environ.get("API_ID", "26513107"))  # Replace 12345 with your default

# Fetch API_HASH with a default empty string
API_HASH = os.environ.get("API_HASH", "f14ce4b58dc8812cfc9665588472f2d4")

# Fetch BOT_TOKEN with a default empty string
BOT_TOKEN = os.environ.get("BOT_TOKEN", "f14ce4b58dc8812cfc9665588472f2d4")

# Fetch PASS_DB or use default value 721
PASS_DB = int(os.environ.get("PASS_DB", "721"))

# Fetch OWNER or use 0 as a default
OWNER = int(os.environ.get("OWNER", "1928404158"))

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



