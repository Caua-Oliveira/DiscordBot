import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice


class Util(commands.Cog):

    def __init__(self, client:commands.Bot) -> None:
        self.client = client

    @app_commands.command(name='avatar', description='Veja a imagem de perfil de alguem!')
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):

        if member == None:

            avatarUrl = interaction.user.avatar.url
            embed = discord.Embed(color=discord.Colour.blue())
            embed.add_field(name=f'🖼 {interaction.user.name}\n ⠀' ,value=f'**Clique [aqui]({avatarUrl}) para baixar a imagem.**', inline=False)
            embed.set_image(url=avatarUrl)

            await interaction.response.send_message(embed=embed)

        else:

            avatarUrl = member.avatar.url
            embed = discord.Embed(color=discord.Colour.blue())
            embed.add_field(name=f'🖼 {member.name}\n ⠀',value=f'**Clique [aqui]({avatarUrl}) para baixar a imagem.**', inline=False)
            embed.set_image(url=avatarUrl)

            await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Util(client))