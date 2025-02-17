import discord
from dotenv import load_dotenv
import os
from comics import get_todays_new_comics
from discord.ext import tasks
from ollamaclient import OllamaClient
from utils import is_it_wednesday

load_dotenv()

class Eris(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role_message_id = None
        self.TOKEN = os.getenv('TOKEN')
        self.SERVER_ID = int(os.getenv('SERVER_ID'))
        self.COMIC_CHANNEL_NAME = "new-comics"
        self.ROLE_CHANNEL_NAME = "roles"
        self.WELCOME_CHANNEL_NAME = "general"
        self.authorized_users = ["pocketspice#9063"]
        self.ROLE_MSG = "React with :monkey: if you want the monkey role."
        self.ollama = self.createOllamaClient()

    def get_channel_id_from_channel_name(self, channel_name):
        channels = self.get_all_channels()
        for channel in channels:
            if channel.name == channel_name:
                return channel.id

    async def setup_roles_channel(self):
        channels = self.get_all_channels()
        role_channel_exists = False
        for channel in channels:
            if channel.name == self.ROLE_CHANNEL_NAME:
                role_channel_exists = True
                print("#" + self.ROLE_CHANNEL_NAME + " already exists")
                break
        if not role_channel_exists:
            server = self.get_guild(self.SERVER_ID)
            await server.create_text_channel(name=self.ROLE_CHANNEL_NAME)
            print("Roles Channel Created")
            role_channel_id = self.get_channel_id_from_channel_name(self.ROLE_CHANNEL_NAME)
            role_channel = self.get_channel(role_channel_id)
            role_message = await role_channel.send(self.ROLE_MSG)
            self.role_message_id = role_message.id
            print('role_message_id set')
        else:
            role_channel_id = self.get_channel_id_from_channel_name(self.ROLE_CHANNEL_NAME)
            role_channel = self.get_channel(role_channel_id)
            member = self.user
            role_message = await discord.utils.get(role_channel.history(limit=1), author=member)
            self.role_message_id = role_message.id
            print('role_message_id set')

    async def comic_command(self, message):
        if str(message.channel) == self.COMIC_CHANNEL_NAME:
            if message.content == "!new comics":
                filename = get_todays_new_comics()
                await message.channel.send(file=discord.File(filename))

    async def on_ready(self):
        await self.wait_until_ready()
        await self.setup_roles_channel()
        print(f'Let the chaos begin!')

    async def welcome_new_member(self, member):
        for channel in member.server.channel:
            if str(channel) == self.WELCOME_CHANNEL_NAME:
                await channel.send(f"Welcome {member.mention}")

    async def on_member_join(self, member):
        await self.welcome_new_member(member)

    async def on_message(self, message):
        server_id = self.get_guild(self.SERVER_ID)
        if str(message.author) in self.authorized_users:
            print(f"valid user {message.author}")
        if message.author.id == self.user.id:
            return
        await self.comic_command(message)
        if message.content.startswith("!hello"):
            await message.reply('Hello!', mention_author=True)
        if message.content == "!users":
            await message.channel.send(f"""# of Members: {server_id.member_count}""")
        if message.content.startswith("!ask"):
            await self.reply_with_ollama_response(message)
        if message.content.startswith("!changeModel"):
            reply = self.changeModel(message)
            await message.reply(reply, mention_author=True)
        if message.content == "!listModels":
            reply = "\n".join(self.ollama.models)
            await message.reply(reply, mention_author=True)

    def createOllamaClient(self):
        return OllamaClient(os.getenv('MODEL'). os.getenv('SYSTEM'))

    def changeModel(self, message):
        newModel = message.content.split(' ')[1]
        if newModel not in self.ollama.models:
            self.ollama.pull_model(newModel)
        modelUpdated = self.ollama.set_model(newModel)
        if not modelUpdated:
            return f"Chat Model {newModel} not found"
        return f"Chat Model updated to {newModel}"

    async def reply_with_ollama_response(self, message):
        message_content = message.content.split(' ')
        query = " ".join(message_content[1:])
        reply = self.ollama.send_chat(message=query)
        await message.reply(reply, mention_author=True)

    async def add_role(self, payload, role_emoji, role_name):
        """
        Give a role to a user when they react with a certain emoji
        :param payload:
        :param role_emoji: emoji to listen for
        :param role_name: role to be added
        :return:
        """
        if payload.message_id != self.role_message_id:
            return
        guild = client.get_guild(payload.guild_id)
        print(payload.emoji.name)
        if payload.emoji.name == role_emoji:
            role = discord.utils.get(guild.roles, name=role_name)
            await payload.member.add_roles(role)

    async def remove_role(self, payload, role_emoji, role_name):
        """
        Remove a role from a user when they react with a certain emoji
        :param payload:
        :param role_emoji: emoji to look for
        :param role_name: role removed
        :return:
        """
        if payload.message_id != self.role_message_id:
            return
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        print(payload.emoji.name)
        if payload.emoji.name == role_emoji:
            role = discord.utils.get(guild.roles, name=role_name)
            await member.remove_roles(role)

    async def on_raw_reaction_add(self, payload):
        await self.add_role(payload, '🐒', 'monkey')

    async def on_raw_reaction_remove(self, payload):
        await self.remove_role(payload, '🐒', 'monkey')

    # background task to check if its wednesday and if it is, post new comics.
    async def setup_hook(self) -> None:
        self.check_if_send_comics.start()

    @tasks.loop(hours=24)
    async def check_if_send_comics(self):
        wed = is_it_wednesday()
        if wed:
            filename = get_todays_new_comics()
            comic_channel_id = self.get_channel_id_from_channel_name(self.COMIC_CHANNEL_NAME)
            channel = client.get_channel(int(comic_channel_id))
            await channel.send(file=discord.File(filename))

    @check_if_send_comics.before_loop
    async def before_check(self):
        await self.wait_until_ready()

