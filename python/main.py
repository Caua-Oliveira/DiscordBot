import discord
import json
from discord.ext import commands, tasks
from itertools import cycle

games = cycle(['Minecraft', 'Hytale', 'Half-Life 3', 'Tetris', 'Roblox', 'Stardew Valley', 'Terraria', 'ULTRAKILL'])

class MyBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix='e!',
            intents = discord.Intents.all(),
            application_id=989409439956213830
        )
        self.initial_extensions = [
            #'commands.anime_commands.anime_command',
            #'commands.anime_commands.waifu_commands',
            #'commands.anime_commands.manga_command',
            #'commands.misc_commands.util',
            #'commands.misc_commands.word_minigame',
            #'commands.help_command.help_command',
            #'commands.misc_commands.matchmaking',
            'commands.misc_commands.img_to_ascii',
        ]
    #Syncing extensions
    async def setup_hook(self):
        for ext in self.initial_extensions:
            await client.load_extension(ext)
        await self.tree.sync()

    async def on_ready(self):
        gameschange.start()
        print('I AM LOGGED IN!')

@tasks.loop(seconds=300)
async def gameschange():
    await client.change_presence(activity=discord.Game(next(games)))

def is_it_me(ctx):  # Commands only i can use
    return ctx.author.id == 325049357063815176

#Starting the bot
client=MyBot()
with open('token.json') as f:
    data = json.load(f)
    TOKEN = data["TOKEN"]

client.run(TOKEN)
