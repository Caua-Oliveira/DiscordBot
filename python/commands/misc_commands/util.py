import discord
import json
from removebg import RemoveBg
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice


class Util(commands.Cog):

    def __init__(self, client:commands.Bot) -> None:
        self.client = client

    @app_commands.command(name='avatar', description="See someone's profile picture!")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):

        if member == None:

            avatarUrl = interaction.user.avatar.url
            embed = discord.Embed(color=discord.Colour.blue())
            embed.add_field(name=f'🖼 {interaction.user.name}\n ⠀' ,value=f'**Click [here]({avatarUrl}) to download the image.**', inline=False)
            embed.set_image(url=avatarUrl)

            await interaction.response.send_message(embed=embed)

        else:

            avatarUrl = member.avatar.url
            embed = discord.Embed(color=discord.Colour.blue())
            embed.add_field(name=f'🖼 {member.name}\n ⠀',value=f'**Click [here]({avatarUrl}) to download the image.**', inline=False)
            embed.set_image(url=avatarUrl)

            await interaction.response.send_message(embed=embed)


    #Removes Background from image
    @app_commands.command(name='remove-background', description="Removes background of a image.")
    async def remove_bg(self, interaction: discord.Interaction, image: discord.Attachment):

        with open('token.json') as f:
            data = json.load(f)
            api_key = data["removebg"]

        rmbg = RemoveBg(api_key, "error.log")
        rmbg.remove_background_from_img_url(image.url)
        try:
            await interaction.response.send_message(file=discord.File('no-bg.png'))
        except:
            await interaction.response.send_message(file=discord.File('no-bg.png'))

    @app_commands.command(name='print', description='Sends Message embed')
    async def print(self, interaction: discord.Interaction, id:str):
        idmsg = int(id)

        try:
            a = await interaction.channel.fetch_message(idmsg)
        except:
            return await interaction.response.send_message('Message Not Found', ephemeral=True)

        embed = discord.Embed(description=a.content,color=discord.Colour.blue(), timestamp=a.created_at.astimezone())
        embed.set_author(name=a.author, icon_url=a.author.avatar.url)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='ping')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message('Pong!')

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Util(client))