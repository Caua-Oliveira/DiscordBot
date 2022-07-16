import discord
import json
import requests
import asyncio
from pprint import pprint
import random
from removebg import RemoveBg
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice


def choose_question():
    questions = {
        'words related to duck that start with the letter b': 'https://api.datamuse.com/words?ml=duck&sp=b*&max=10',
        'words related to spoon that end with the letter a': 'https://api.datamuse.com/words?ml=spoon&sp=*a&max=10',
        'words that rhyme with jail': 'https://api.datamuse.com/words?rel_rhy=jail',
        'adjectives that are often used to describe ocean': 'https://api.datamuse.com/words?rel_jjb=ocean'}

    question, answers = random.choice(list(questions.items()))
    return question, answers



class WordGame(commands.Cog):

    def __init__(self, client:commands.Bot) -> None:
        self.client = client

    async def repeat(self, interaction: discord.Interaction, question: str, answers:str):
        r = requests.get(answers)
        r = r.json()
        await interaction.channel.send(question)

        def check(m):
            for i in range(len(r)):
                if m.content == r[i]['word']:
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

        dic = {'Trapyy': 0, 'Others': 0}

        question,answers = choose_question()
        a = await self.repeat(interaction, question, answers)
        if a == 'Trapyy':
            dic['Trapyy']+=1
        else:
            dic['fake']+=1
        b = await self.repeat(interaction, question, answers)
        if b == 'Trapyy':
            dic['Trapyy']+=1
        else:
            dic['fake']+=1

        print(dic)
        await interaction.channel.send(str(dic))






















async def setup(client: commands.Bot) -> None:
    await client.add_cog(WordGame(client))