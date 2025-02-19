from bot.eris import Eris
from discord import Intents
import logging
import bot.settings

if __name__ == "__main__":
    print(bot.settings.LOG_PATH)
    print(bot.settings.ROOT_DIR)
    golden_intentions = Intents.default()
    golden_intentions.message_content = True
    golden_intentions.members = True
    golden_intentions.reactions = True
    client = Eris(intents=golden_intentions)
    client.run(client.get_token())