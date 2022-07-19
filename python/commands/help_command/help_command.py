import discord
import json
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

helpCommands = json.load(open("help.json"))

def help_embed(page):
    pageTitle = list(helpCommands)[page]
    embed = discord.Embed(colour=discord.Colour.blue(), title=pageTitle, description="ㅤ")
    for key, val in helpCommands[pageTitle].items():
        embed.add_field(name=key, value=val, inline=False)
    embed.set_footer(text=f"Page: {page+1}/{len(list(helpCommands))}" )
    return embed

class HelpButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=90.0)
        self.response = None


    async def on_timeout(self) -> None:  # Deactivate buttons after timeout
        for child in self.children:
            child.disabled = True
        await self.response.edit(view=self)

    @discord.ui.button(label='🎭', style=discord.ButtonStyle.blurple)
    async def anime_things(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.edit_message(embed=help_embed(0))

    @discord.ui.button(label='🔧', style=discord.ButtonStyle.blurple)
    async def utilities(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.edit_message(embed=help_embed(1))

    @discord.ui.button(label='🎮', style=discord.ButtonStyle.blurple)
    async def minigames(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.edit_message(embed=help_embed(2))

    @discord.ui.button(label='📖', style=discord.ButtonStyle.blurple)
    async def menu(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.edit_message(embed=self.response)


class HelpCommand(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name='tpan-help')
    async def tpan_help(self, interaction: discord.Interaction):
        pageTitles = list(helpCommands)
        embed = discord.Embed(colour=discord.Colour.blue(), title="Down bellow it's all my commands, have fun!", description= 'ㅤ')
        embed.set_author(name="Help Menu", icon_url="https://twemoji.maxcdn.com/2/72x72/1f4d6.png")
        for x in pageTitles:
            embed.add_field(name=x, value =' • '.join(f"`{y}`" for y in helpCommands[x]), inline=False)

        view = HelpButtons()
        await interaction.response.send_message(embed=embed, view=view)
        original_embed = embed
        view.response = original_embed



async def setup(client: commands.Bot) -> None:
    await client.add_cog(HelpCommand(client))