import discord
from dotenv import load_dotenv
import os
from comics import get_todays_new_comics
from discord.ext import tasks
import datetime

load_dotenv()

class Eris(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SERVER_ID = int(os.getenv('SERVER_ID'))
        self.COMIC_CHANNEL_NAME = "new-comics"
        self.ROLE_CHANNEL_NAME = "roles"
        self.WELCOME_CHANNEL_NAME = "general"
        self.authorized_users = ["pocketspice#9063"]
        self.ROLE_MSG = "React with :monkey: if you want the monkey role."

    async def setup_hook(self) -> None:
        self.check_if_its_wednesday.start()

    @tasks(seconds=86400)
    async def check_if_its_wednesday(self):
        if datetime.today().weekday() == 2:
            comic_command()

    @check_if_its_wednesday.before_loop
    async def before_date_check(self):
        await self.wait_until_ready()

    async def commic_command(self):
        channel_id = get_channel_id_from_channel_name(self.COMIC_CHANNEL_NAME)
        channel = client.get_channel(int(channel_id))
        get_todays_new_comics()
        await channel.send(file=discord.File('comics.txt'))

    def get_channel_id_from_channel_name(self, channel_name):
        channels = client.get_all_channels()
        for channel in channels:
            if channel.name == self.ROLE_CHANNEL_NAME:
                return channel.id

    async def setup_roles_channel(self):
        channels = client.get_all_channels()
        role_channel_exists = False
        for channel in channels:
            if channel.name == self.ROLE_CHANNEL_NAME:
                role_channel_exists = True
                print("#" + self.ROLE_CHANNEL_NAME + " already exists")
                break
        if not role_channel_exists:
            server = client.get_guild(self.SERVER_ID)
            await server.create_text_channel(name=self.ROLE_CHANNEL_NAME)
            print("Roles Channel Created")
            role_channel_id = self.get_channel_id_from_channel_name(self.ROLE_CHANNEL_NAME)
            role_channel = client.get_channel(role_channel_id)
            role_message = await role_channel.send(self.ROLE_MSG)
            self.role_message_id = role_message.id
            print('role_message_id set')
        else:
            role_channel_id = self.get_channel_id_from_channel_name(self.ROLE_CHANNEL_NAME)
            role_channel = client.get_channel(role_channel_id)
            member = client.user
            role_message = await discord.utils.get(role_channel.history(limit=1), author=member)
            self.role_message_id = role_message.id
            print('role_message_id set')

    async def on_ready(self):
        await client.wait_until_ready()
        await self.setup_roles_channel()
        print(f'Let the chaos begin!')

    async def welcome_new_member(self, member):
        for channel in member.server.channel:
            if str(channel) == self.WELCOME_CHANNEL_NAME:
                await client.send_message(f"Welcome {member.mention}")

    async def on_member_join(self, member):
        global joins
        joins += 1
        await self.welcome_new_member(member)

    async def on_message(self, message):
        global messages
        messages += 1
        id = client.get_guild(self.SERVER_ID)
        if str(message.author) in self.authorized_users:
            print(f"valid user {message.author}")
        if message.author.id == self.user.id:
            return
        if message.content.startswith("!hello"):
            await message.reply('Hello!', mention_author=True)
        if message.content == "!users":
            await message.channel.send(f"""# of Members: {id.member_count}""")

    async def add_role(self, payload, role_emoji, role_name):
        '''
        Give a role to a user when they react with a certain emoji
        :param payload:
        :param role_emoji: emoji to listen for
        :param role_name: role to be added
        :return:
        '''
        if payload.message_id != self.role_message_id:
            return
        guild = client.get_guild(payload.guild_id)
        print(payload.emoji.name)
        if payload.emoji.name == role_emoji:
            role = discord.utils.get(guild.roles, name=role_name)
            await payload.member.add_roles(role)

    async def remove_role(self, payload, role_emoji, role_name):
        '''
        Remove a role from a user when they react with a certain emoji
        :param payload:
        :param role_emoji: emoji to look for
        :param role_name: role removed
        :return:
        '''
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



golden_intentions = discord.Intents.default()
golden_intentions.message_content = True
golden_intentions.members = True
golden_intentions.reactions = True
client = Eris(intents=golden_intentions)
client.run(os.getenv('TOKEN'))
