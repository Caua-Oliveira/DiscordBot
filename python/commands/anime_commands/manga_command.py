import discord
import requests
from discord import app_commands
from discord.ext import commands
from pprint import pprint

def get_anime(page: int, search: str):

    query = '''
    query ($id: Int, $page: Int, $perPage: Int, $search: String) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media (id: $id, search: $search, type: MANGA) {
                id
                title {
                    romaji
                    english
                }
                idMal
                format
                type
                status
                description
                startDate{
                    year
                    month
                    day
                }
                chapters
                volumes
                duration
                source
                coverImage{
                    large
                    color
                }
                bannerImage
                genres
                synonyms
                meanScore
                studios(isMain: true){
                    nodes{
                        name
                    }
                }
                isAdult
                nextAiringEpisode{
                    airingAt
                }
                siteUrl
                }
            }

    }


    '''
    variables = {
        'search': search,
        'page': 1,
        'perPage': 10
    }

    url = 'https://graphql.anilist.co'

    response = requests.post(url, json={'query': query, 'variables': variables})
    response = response.json()

    titleR = response['data']['Page']['media'][page]['title']['romaji']
    titleE = response['data']['Page']['media'][page]['title']['english']
    bannerImage = response['data']['Page']['media'][page]['bannerImage']
    coverImage = response['data']['Page']['media'][page]['coverImage']['large']
    description = response['data']['Page']['media'][page]['description'][0:671].replace('<br>', ' ').replace('<i>', '').replace('</i>', '') + '**. . .**'
    chapters = str(response['data']['Page']['media'][page]['chapters'])
    if chapters == None: chapters = 'N/A'
    volumes = str(response['data']['Page']['media'][page]['volumes'])
    format = response['data']['Page']['media'][page]['format']
    genres = response['data']['Page']['media'][page]['genres']
    idMal = response['data']['Page']['media'][page]['idMal']
    mal = f'https://myanimelist.net/manga/{idMal}'
    isAdult = 'Yes' if response['data']['Page']['media'][page]['isAdult'] else 'No'
    meanScore = str(response['data']['Page']['media'][page]['meanScore']) + '/100'
    try:
        nextAiring = response['data']['Page']['media'][page]['nextAiringEpisode']['airingAt']
    except TypeError as type_error:
        print(type_error)
        nextAiring = response['data']['Page']['media'][page]['nextAiringEpisode']
    anilist = response['data']['Page']['media'][page]['siteUrl']
    try:
        source = response['data']['Page']['media'][page]['source'].lower().capitalize().replace('_', ' ')
    except AttributeError as attribute_error:
        print(attribute_error)
        source = 'N/A'
    dates = ['day', 'month', 'year']
    startDate = ''.join(str([response['data']['Page']['media'][page]['startDate'][y] for y in dates])).replace(']','').replace('[', '').replace(', ', '/')
    if 'None' in startDate: startDate = 'N/A'
    status = response['data']['Page']['media'][page]['status'].lower().capitalize().replace('_', ' ')
    synonyms = response['data']['Page']['media'][page]['synonyms']
    entries = len(response['data']['Page']['media'])

    # EMBED______________________________________________________________________________________________

    embed = discord.Embed(title=f"{titleR} ({titleE})", url=anilist, description=description, color=discord.Colour.blue())
    embed.set_author(name=f"Type: {format} • Status: {status} • Score: {meanScore}",
                     icon_url='https://media.discordapp.net/attachments/978016869342658630/978033399107289189/anilist.png')
    embed.set_image(url=bannerImage)
    embed.set_thumbnail(url=coverImage)
    embed.add_field(name="**Chapters**", value=f'`{chapters}`', inline=True)
    embed.add_field(name="**Volumes**", value=f'`{volumes}`', inline=True)
    embed.add_field(name="**Release date**", value=f'`{startDate}`', inline=False)
    embed.add_field(name="**Sourceㅤ**", value=f'`{source}`', inline=True)
    embed.add_field(name="**Genres**", value=' • '.join(f'`{x}`' for x in genres), inline=False)
    embed.add_field(name="**Alternative names**", value=' • '.join(f'`{x}`' for x in synonyms) if len(synonyms)>0 else '`N/A`', inline=False)
    embed.add_field(name="**Find more**", value=f"[Myanimelist Page]({mal})\n[Anilist Page]({anilist})", inline=False)
    embed.set_footer(text=f"Provided by https://anilist.co/  •  Page: {page + 1}/{entries} ")

    return embed


# Buttons from anime command
class PassButttons(discord.ui.View):
    def __init__(self, page: int, search: str, entries: int):
        super().__init__(timeout=30.0)
        self.response = None
        self.page = page
        self.search = search
        self.entries = entries

        next = [x for x in self.children if x.custom_id == 'next'][0]
        last = [x for x in self.children if x.custom_id == 'last'][0]
        deactivate = [x for x in self.children if x.custom_id == 'deactivate'][0]
        if self.page == self.entries - 1:
            next.disabled = True
            last.disabled = True
            deactivate.disabled = True


    async def on_timeout(self) -> None:  # Deactivate buttons after timeout
        for child in self.children:
            child.disabled = True
        await self.response.edit(view=self)


    # First Entrie
    @discord.ui.button(label='«', style=discord.ButtonStyle.blurple, custom_id='first', disabled=True)
    async def first(self, interaction: discord.Interaction, button: discord.ui.Button):
        first = [x for x in self.children if x.custom_id == 'first'][0]
        previous = [x for x in self.children if x.custom_id == 'previous'][0]
        next = [x for x in self.children if x.custom_id == 'next'][0]
        last = [x for x in self.children if x.custom_id == 'last'][0]
        self.page = 0
        first.disabled = True
        previous.disabled = True
        next.disabled = False
        last.disabled = False
        await self.response.edit(view=self)
        await interaction.response.edit_message(embed=get_anime(self.page, self.search))

    # Previous Entrie
    @discord.ui.button(label='◀', style=discord.ButtonStyle.blurple, custom_id='previous', disabled=True)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        first = [x for x in self.children if x.custom_id == 'first'][0]
        previous = [x for x in self.children if x.custom_id == 'previous'][0]
        next = [x for x in self.children if x.custom_id == 'next'][0]
        last = [x for x in self.children if x.custom_id == 'last'][0]
        self.page -= 1
        next.disabled = False
        last.disabled = False
        if self.page==0:
            first.disabled=True
            previous.disabled=True

        await self.response.edit(view=self)
        await interaction.response.edit_message(embed=get_anime(self.page, self.search))

    # Next Entrie
    @discord.ui.button(label='▶', style=discord.ButtonStyle.blurple, custom_id='next')
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        first = [x for x in self.children if x.custom_id == 'first'][0]
        previous = [x for x in self.children if x.custom_id == 'previous'][0]
        next = [x for x in self.children if x.custom_id == 'next'][0]
        last = [x for x in self.children if x.custom_id == 'last'][0]
        self.page += 1
        first.disabled = False
        previous.disabled = False
        if self.page==self.entries-1:
            next.disabled = True
            last.disabled = True
        await self.response.edit(view=self)
        await interaction.response.edit_message(embed=get_anime(self.page, self.search))

    # Last Entrie
    @discord.ui.button(label='»', style=discord.ButtonStyle.blurple, custom_id='last')
    async def last(self, interaction: discord.Interaction, button: discord.ui.Button):
        first = [x for x in self.children if x.custom_id == 'first'][0]
        previous = [x for x in self.children if x.custom_id == 'previous'][0]
        next = [x for x in self.children if x.custom_id == 'next'][0]
        last = [x for x in self.children if x.custom_id == 'last'][0]
        self.page = self.entries - 1
        next.disabled = True
        last.disabled = True
        first.disabled = False
        previous.disabled = False
        await self.response.edit(view=self)
        await interaction.response.edit_message(embed=get_anime(self.page, self.search))

    # Deactivate buttons
    @discord.ui.button(label="✖", style=discord.ButtonStyle.red, custom_id='deactivate')
    async def disable_all_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(view=self)


class Manga_Command(commands.Cog):

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    # ANIME COMMAND INFO
    @app_commands.command(name='manga', description='Searchs for an anime and display information about it!')
    @app_commands.describe(search='Name of the anime')
    async def manga(self, interaction: discord.Interaction, search: str):
        page = 0
        #query request
        query = '''
            query ($id: Int, $page: Int, $perPage: Int, $search: String) {
                Page (page: $page, perPage: $perPage) {
                    pageInfo {
                        total
                    }
                    media (id: $id, search: $search, type: MANGA) {
                        id
                    }
            }
    }   
'''
        variables = {
            'search': search,
            'page': 1,
            'perPage': 10
        }
        url = 'https://graphql.anilist.co'
        response = requests.post(url, json={'query': query, 'variables': variables})
        response = response.json()

        entries = len(response['data']['Page']['media'])


        # Button call
        view = PassButttons(page, search, entries)
        await interaction.response.send_message(embed=get_anime(page, search), view=view)
        out = await interaction.original_message()
        view.response = out




async def setup(client: commands.Bot) -> None:
    await client.add_cog(Manga_Command(client))
