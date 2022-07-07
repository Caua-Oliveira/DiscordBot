import discord
import requests
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

class ReloadButton(discord.ui.View):
    def __init__(self, filtro:str, categoria:str):
        super().__init__()
        self.filtro=filtro
        self.categoria=categoria

    @discord.ui.button(label='🔄', style=discord.ButtonStyle.blurple)
    async def reload(self, interaction: discord.Interaction, button: discord.ui.Button):
        r = requests.get(f'https://api.waifu.pics/{self.filtro}/{self.categoria}')
        content = r.text[8:-3]
        await interaction.response.edit_message(content=content)

class WaifuCommands(commands.Cog):

    def __init__(self, client:commands.Bot) -> None:
        self.client = client

#WAIFU COMMAND
    @app_commands.command(name='waifu', description='Gere imagens de waifus!')
    @app_commands.describe(
        filtro='SFW or NSFW',
        categoria = 'Categoria da imagem')
    @app_commands.choices(filtro= [
        Choice(name='sfw', value='sfw'),
        Choice(name='nsfw', value='nsfw')],
        categoria=[
            Choice(name='waifu', value='waifu'),
            Choice(name='neko', value='neko'),
            Choice(name='smile', value='smile')
            ])
    async def waifu(self, interaction: discord.Interaction,filtro:str,categoria:str):
        r = requests.get(f'https://api.waifu.pics/{filtro}/{categoria}')
        content = r.text[8:-3]
        view = ReloadButton(filtro,categoria)
        await interaction.response.send_message(content, view=view)
        await view.wait()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(WaifuCommands(client))



