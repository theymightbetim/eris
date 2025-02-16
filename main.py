from eris import Eris
from discord import Intents

if __name__ == "__main__":
    golden_intentions = Intents.default()
    golden_intentions.message_content = True
    golden_intentions.members = True
    golden_intentions.reactions = True
    client = Eris(intents=golden_intentions)
    client.run(client.TOKEN)