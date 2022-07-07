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

    @discord.ui.button(label='gerar', style=discord.ButtonStyle.blurple)
    async def reload(self, interaction: discord.Interaction, button: discord.ui.Button):
        r = requests.get(f'https://api.waifu.pics/{self.filtro}/{self.categoria}')
        content = r.text[8:-3]
        embed = discord.Embed(color=discord.Colour.blue())
        embed.set_author(name=f'{self.filtro.upper()} • {self.categoria.capitalize()}')
        embed.set_image(url=content)
        await interaction.response.edit_message(embed=embed)

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
        embed = discord.Embed(color=discord.Colour.blue())
        embed.set_author(name=f'{filtro.upper()} • {categoria.capitalize()}')
        embed.set_image(url=content)
        await interaction.response.send_message(embed=embed, view=view)
        await view.wait()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(WaifuCommands(client))



