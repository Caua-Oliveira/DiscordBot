import discord
import requests
from pprint import pprint
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice


class MalCommands(commands.Cog):

    def __init__(self, client:commands.Bot) -> None:
        self.client = client

#ANIME COMMAND
    @app_commands.command(name='anime', description='Ache informações sobre animes!')
    @app_commands.describe(
        filtro='SFW or NSFW',
        nome='Nome do anime')
    @app_commands.choices(filtro=[
        Choice(name='sfw', value='sfw'),
        Choice(name='nsfw', value='nsfw')])
    async def anime(self, interaction: discord.Interaction,filtro:str,nome:str):
        page=0
        r = requests.get(f'http://staging.jikan.moe/v4/anime?q={nome}&{filtro}')
        t = r.json()
        url = t['data'][page]['url']
        mal='https://cdn.discordapp.com/attachments/989374831487229952/993011826109448223/unknown.png'
        title = t['data'][page]['title']
        score = t['data'][page]['score']
        if score == None:
            score = '??'
        image = t['data'][page]['images']['jpg']['image_url']
        episodes = str(t['data'][page]['episodes'])
        duration = t['data'][page]['duration']
        aired = t['data'][page]['aired']['string']
        source = t['data'][page]['source']
        try:
            studio = t['data'][page]['studios'][0]['name']
        except IndexError as index_error:
            print(index_error)
            studio = 'Não expecificado'
        genres = [t['data'][page]['genres'][generos]['name'] for generos in range(len(t['data'][page]['genres']))]
        if len(genres) == 0:
            genres.append('Não expecificado')
        synopsis = t['data'][page]['synopsis'][:-25]
        rank = t['data'][page]['rank']
        synonyms = t['data'][page]['title_synonyms']
        english_title = t['data'][page]['title_english']
        if english_title != None:
            synonyms.insert(0, english_title)
        else:
            english_title = ' '
        japanese_title = t['data'][page]['title_japanese']
        if japanese_title != None:
            synonyms.append(japanese_title)
        else:
            pass
        status = t['data'][page]['status']
        type = t['data'][page]['type']


        embed = discord.Embed(title=f"{title} ({english_title})", url=url, description=synopsis,color=discord.Colour.blue())
        embed.set_author(name=f"Tipo: {type} • Status: {status} • Nota: {score} • Rank: {rank}",
                         icon_url=mal)
        embed.set_thumbnail(
            url=image)
        embed.add_field(name="**Episódios**", value=f'`{episodes}`', inline=True)
        embed.add_field(name="**Duração**", value=f'`{duration}`', inline=True)
        embed.add_field(name="**Data de lançamento**", value=f'`{aired}`', inline=False)
        embed.add_field(name="**Fonteㅤ**", value=f'`{source}`', inline=True)
        embed.add_field(name="**Estúdio**", value=f'`{studio}`', inline=True)
        embed.add_field(name="**Gêneros**", value=' • '.join(f'`{x}`' for x in genres), inline=False)
        embed.add_field(name="**Nomes alternativos**", value=' • '.join(f'`{x}`' for x in synonyms), inline=False)
        embed.add_field(name="**Saiba mais**", value=f"[Myanimelist Page]({url})", inline=False)
        embed.set_footer(icon_url='https://cdn.discordapp.com/avatars/989409439956213830/b9336d36eb09936ca2405830600c1bc3.webp?size=1024', text="De: myanimelist.com")
        await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(MalCommands(client))