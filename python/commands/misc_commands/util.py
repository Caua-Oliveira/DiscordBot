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

        await interaction.response.send_message(file=discord.File('no-bg.png'))


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Util(client))