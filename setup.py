import sys
import subprocess

# install requirements.txt:
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                       '-r', 'requirements.txt'])

# ask fo env variables and save to .env file
print("Please enter your bot token from discord developer settings")
token = input("Bot Token: ")
print("Please enter your bots token from discord developer settings")
app_id = input("Application ID: ")
print("Please enter your Guild/Server ID from the discord server.")
server_id = input("Server ID: ")
print('Calculate Bot Permission Integer: https://discordapi.com/permissions.html')
permissions_number = input("Permission Integer: ")

VARS = f'''TOKEN={token}
PERMISSION_INTEGER={permissions_number}
APPLICATION_ID={app_id}
SERVER_ID={server_id}
'''

with open('.env', 'w') as f:
    f.write(VARS)

link = f'https://discord.com/api/oauth2/authorize?client_id={app_id}&permissions={permissions_number}'
print("Click this link to invite the bot to your server")
print(link)
