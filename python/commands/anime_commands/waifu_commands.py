import discord
import requests
import urllib.parse
from saucenao_api import SauceNao
from pprint import pprint
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



    @app_commands.command(name='find-anime-episode', description="Find the anime episode/name by the image that you use!")
    async def find_anime_episode(self, interaction: discord.Interaction, image: discord.Attachment):

        await interaction.response.defer()
        image = image.url
        r = requests.get("https://api.trace.moe/search?url={}".format(urllib.parse.quote_plus(image))).json()
        if r['error'] != '':
            return await interaction.response.send_message('Queue is full', ephemeral=True)
        image2 = r['result'][0]['image']
        episode = r['result'][0]['episode']
        video = r['result'][0]['video']
        id = r['result'][0]['anilist']
        anilist = f'https://anilist.co/anime/{str(id)}/'
        similarity = r['result'][0]['similarity'] * 100
        similarity = "{:.2f}".format(similarity)

        #Find Anime Name
        query = '''
            query ($id: Int) { # Define which variables will be used in the query (id)
                Media (id: $id, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
                id
                title {
                    romaji
                    english
                    native
                }
                idMal
                }
            }
            '''

        # Define our query variables and values that will be used in the query request
        variables = {
            'id': id
        }
        url = 'https://graphql.anilist.co'
        # Make the HTTP Api request
        response = requests.post(url, json={'query': query, 'variables': variables})
        title = response.json()['data']['Media']['title']['english']
        idmal = response.json()['data']['Media']['idMal']
        myanimelist = f'https://myanimelist.net/anime/{idmal}'

        # Embed

        embed = discord.Embed(description=f"Title: **{title}** \nSimilarity: **{similarity}%** \nEpisode: **{episode}**  \nShort Clip: [**Link**]({video})  \nAnilist: [**Link**]({anilist})  \nMyanimelist: [**Link**]({myanimelist})",color=discord.Colour.blue())
        embed.set_author(name="That's what i've found!",icon_url="https://cdn.discordapp.com/avatars/989409439956213830/b9336d36eb09936ca2405830600c1bc3.png?size=1024")
        embed.set_image(url=image2)
        embed.set_footer(icon_url=interaction.user.avatar.url, text=f'Requested by: {interaction.user.name}')

        await interaction.edit_original_message(embed=embed)

    @app_commands.command(name='find-original-art', description="Find original art/artist by the image that you use!")
    async def find_original_art(self, interaction: discord.Interaction, image: discord.Attachment):
        sauce = SauceNao('24920e17f404cf78f146f3773d38c68424bf33c6').from_url(image.url)

        thumb = sauce[0].thumbnail
        similarity = sauce[0].similarity
        title = sauce[0].title
        urls = sauce[0].urls
        dict = {}
        for x in urls:
            if 'danbooru' in x:
                dict['danbooru'] = x
            elif 'gelbooru' in x:
                dict['gelbooru'] = x
            elif 'yande.re' in x:
                dict['yande.re'] = x
            elif 'artstation' in x:
                dict['artstation'] = x
        author = sauce[0].author
        try:
            source = sauce.raw['results'][0]['data']['source']
        except:
            source = False
        embed = discord.Embed(color=discord.Colour.blue())
        embed.set_author(name=f'Titles: {title} • Similarity: {similarity}',
                         icon_url='https://cdn.discordapp.com/attachments/989647128139808869/998717737452978226/unknown.png')
        embed.set_image(url=thumb)
        embed.add_field(name='**Author:**', value=author, inline=False)
        embed.add_field(name='**Urls:**', value=''.join(f"[{x}]({y})\n" for x,y in dict.items()), inline=False)
        embed.set_footer(text=f"Provided by https://saucenao.com/ ")
        if source:
            embed.add_field(name='**Source:**', value=f'[Original post]({source})', inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(WaifuCommands(client))



