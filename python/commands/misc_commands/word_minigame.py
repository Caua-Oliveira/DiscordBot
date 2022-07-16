import discord
import requests
import json
import asyncio
import random
from discord import app_commands
from discord.ext import commands



def choose_question():

    with open('questions.json') as f:
        questions = json.load(f)

    question, answer = random.choice(list(questions.items()))
    return question, answer


class WordGame(commands.Cog):

    def __init__(self, client:commands.Bot) -> None:
        self.client = client

    async def repeat(self, interaction: discord.Interaction, question: str, answers:str):
        r = requests.get(answers)
        r = r.json()
        embed = discord.Embed(title='Question:', description=f'{question}',color=discord.Colour.blue())
        await interaction.channel.send(embed=embed)

        def check(m):
            for i in range(len(r)):
                if m.content.lower().strip() == r[i]['word']:
                    return True
            return False

        msg = await self.client.wait_for('message', check=check)
        await interaction.channel.send(f'+1 point for {msg.author.mention}')
        return msg.author.name



    @app_commands.command(name='word-game')
    async def wordgame(self, interaction: discord.Interaction):
        await interaction.response.send_message('The game will Start!')
        await asyncio.sleep(5)
        await interaction.edit_original_message(content='The game started!')

        dic = {}

        question, answer = choose_question()
        a = await self.repeat(interaction, question, answer)
        if a in dic:
            dic[f'{a}']+=1
        else:
            dic[a]=1
        question, answer = choose_question()
        b = await self.repeat(interaction, question, answer)
        if b in dic:
            dic[f'{b}'] += 1
        else:
            dic[b] = 1
        question, answer = choose_question()
        c = await self.repeat(interaction, question, answer)
        if c in dic:
            dic[f'{c}'] += 1
        else:
            dic[c] = 1
        question, answer = choose_question()
        d = await self.repeat(interaction, question, answer)
        if d in dic:
            dic[f'{d}'] += 1
        else:
            dic[d] = 1
        question, answer = choose_question()
        e = await self.repeat(interaction, question, answer)
        if e in dic:
            dic[f'{e}'] += 1
        else:
            dic[e] = 1

        sortedD = dict(sorted(dic.items(),
                                  key=lambda item: item[1],
                                  reverse=True))

        await interaction.channel.send('Game Ended! Waiting for results')
        await asyncio.sleep(3)

        players = [f"`{i}`" for i in list(sortedD.keys())]
        points = [f"{i}" for i in list(sortedD.values())]

        embed = discord.Embed(title= f"🏆Congratulations @{list(sortedD.keys())[0]}🏆\nﾠ",color=discord.Colour.blue())
        embed.set_author(name=f"We have a winner!\n",icon_url="https://cdn.discordapp.com/avatars/989409439956213830/b9336d36eb09936ca2405830600c1bc3.png?size=1024")
        embed.set_image(url="https://cdn.discordapp.com/attachments/808294539739529236/997973698575351859/no-bg.png")
        embed.add_field(name="Scoreboard", value= '\n'.join(f"{players[o]}- **{points[o]}**" for o in range(len(players))),inline=False)

        await interaction.channel.send(embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(WordGame(client))