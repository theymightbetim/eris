import flake8.defaults
from bot.eris import Eris
from discord import Intents
import bot.settings

if __name__ == "__main__":
    golden_intentions = Intents.default()
    golden_intentions.message_content = True
    golden_intentions.members = True
    golden_intentions.reactions = True
    client = Eris(intents=golden_intentions)
    client.run(client.get_token())
