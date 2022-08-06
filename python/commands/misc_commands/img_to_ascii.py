import discord
from PIL import Image
from io import BytesIO
import requests
from discord import app_commands
from discord.ext import commands

ascii_chars =['@', '#', 'S', '&', '?', '*', '+', ';', ':', ',', '.']


def download(url, filename):
    r = requests.get(url)
    im = Image.open(BytesIO(r.content))
    im.save(filename)
    img = Image.open(r'ascii.png')
    return img

def resize(img):
    resized_img = img.resize((64,25))
    return resized_img

def turn_to_gray(img):
    grey_img = img.convert("L")
    return grey_img

def to_ascii(img):
    pixels = img.getdata()
    charset = ' ˑ.\'-",:;~+*iloöõB@'
    chars = ''
    for pixel in pixels:
        chars += charset[round(get_index(pixel, 0, 255, 0, len(charset) - 1))]
    return chars

def get_index(number, inMin, inMax, outMin, outMax):
    return (number - inMin) * (outMax - outMin) / (inMax - inMin) + outMin


class Img_Ascii(commands.Cog):

    def __init__(self, client:commands.Bot) -> None:
        self.client = client

    @app_commands.command(name='image-to-ascii', description="See someone's profile picture!")
    async def image_to_ascii(self, interaction: discord.Interaction, image: discord.Attachment):
        await interaction.response.defer()
        img = download(image.url, 'ascii.png')
        new_img_data = to_ascii(turn_to_gray((resize(img))))
        ascii_img = '\n'.join(new_img_data[i:i + 64] for i in range(0, len(new_img_data), 64))
        print(ascii_img)
        await interaction.edit_original_message(content = f'```{ascii_img}```\n')
        await interaction.channel.send(file = discord.File('ascii.png'))





async def setup(client: commands.Bot) -> None:
    await client.add_cog(Img_Ascii(client))