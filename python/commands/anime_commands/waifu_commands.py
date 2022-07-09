import discord
import requests
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

class ReloadButton(discord.ui.View):
    def __init__(self, categoria:str):
        super().__init__(timeout=30.0)
        self.categoria=categoria
        self.response=None

    async def on_timeout(self) -> None:  #Deactivate buttons after timeout
        for child in self.children:
            child.disabled = True
        await self.response.edit(view=self)

    @discord.ui.button(label='Gerar', style=discord.ButtonStyle.blurple)
    async def reload(self, interaction: discord.Interaction, button: discord.ui.Button):
        r = requests.get(f'https://api.waifu.pics/sfw/{self.categoria}')
        content = r.text[8:-3]
        embed = discord.Embed(color=discord.Colour.blue())
        embed.set_author(name=f'SFW • {self.categoria.capitalize()}')
        embed.set_image(url=content)
        await interaction.response.edit_message(embed=embed)

class WaifuCommands(commands.Cog):

    def __init__(self, client:commands.Bot) -> None:
        self.client = client

#WAIFU COMMAND INFO
    @app_commands.command(name='waifu', description='Gere imagens de waifus!')
    @app_commands.describe(
        categoria = 'Categoria da imagem')
    @app_commands.choices(
        categoria=[
            Choice(name='waifu', value='waifu'),
            Choice(name='neko', value='neko'),
            Choice(name='smile', value='smile'),
            Choice(name='hug', value='hug'),
            Choice(name='cuddle', value='cuddle'),
            Choice(name='cry', value='cry'),
            Choice(name='bully', value='bully'),
            Choice(name='kiss', value='kiss'),
            Choice(name='pat', value='pat'),
            Choice(name='smug', value='smug'),
            Choice(name='bonk', value='bonk'),
            Choice(name='blush', value='blush'),
            Choice(name='dance', value='dance'),
            Choice(name='poke', value='poke'),
            Choice(name='wink', value='wink'),
            Choice(name='megumin', value='megumin'),
            Choice(name='happy', value='happy'),
            Choice(name='kick', value='kick'),
            Choice(name='slap', value='slap'),
            Choice(name='bite', value='bite'),
            Choice(name='nom', value='nom'),
            Choice(name='wave', value='wave')
        ]
    )

    #execute
    async def waifu(self, interaction: discord.Interaction,categoria:str):
        r = requests.get(f'https://api.waifu.pics/sfw/{categoria}')
        content = r.text[8:-3]

        embed = discord.Embed(color=discord.Colour.blue())
        embed.set_author(name=f'SFW • {categoria.capitalize()}')
        embed.set_image(url=content)

        view = ReloadButton(categoria)
        await interaction.response.send_message(embed=embed, view=view)
        out = await interaction.original_message()
        view.response = out



async def setup(client: commands.Bot) -> None:
    await client.add_cog(WaifuCommands(client))



