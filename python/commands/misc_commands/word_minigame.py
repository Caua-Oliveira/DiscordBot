import discord
import requests
import json
import asyncio
import random
from discord import app_commands
from discord.ext import commands

with open('questions.json') as f:
    questions = json.load(f)

def choose_question(questions): #Chooses the questions randomly

    question, answer = random.choice(list(questions.items()))
    del questions[question]
    return question, answer


class WordGame(commands.Cog):

    def __init__(self, client:commands.Bot) -> None:
        self.client = client

    #Sends question to the channel and wait for the correct answer
    async def handle_answers_round(self, interaction: discord.Interaction, question: str, answer:str):
        api_response = requests.get(answer)
        answers = api_response.json()
        embed = discord.Embed(title='Question:', description=f'{question}',color=discord.Colour.blue())
        await interaction.channel.send(embed=embed)

        def is_correct_answer(message):
            for word in range(len(answers)):
                if message.content.lower().strip() == answers[word]['word']:
                    return True
            return False

        message = await self.client.wait_for('message', check=is_correct_answer)
        await interaction.channel.send(f'+1 point for {message.author.mention}')
        return message.author.name


    #Minigame command
    @app_commands.command(name='word-game')
    async def wordgame(self, interaction: discord.Interaction):
        with open('questions.json') as f:
            questions = json.load(f)

        await interaction.response.send_message('The game will Start!')
        await asyncio.sleep(5)
        await interaction.edit_original_message(content='The game started!')

        scoreboard = {}

        #Calling the functions to choose and send the questions
        question, answer = choose_question(questions)
        correct_guesser = await self.handle_answers_round(interaction, question, answer)
        #Add correct guesser to scoreboard or add 1 point to them
        scoreboard[correct_guesser]=1

        question, answer = choose_question(questions)
        correct_guesser = await self.handle_answers_round(interaction, question, answer)
        if correct_guesser in scoreboard:
            scoreboard[f'{correct_guesser}'] += 1
        else:
            scoreboard[correct_guesser] = 1

        question, answer = choose_question(questions)
        correct_guesser = await self.handle_answers_round(interaction, question, answer)
        if correct_guesser in scoreboard:
            scoreboard[f'{correct_guesser}'] += 1
        else:
            scoreboard[correct_guesser] = 1

        question, answer = choose_question(questions)
        correct_guesser = await self.handle_answers_round(interaction, question, answer)
        if correct_guesser in scoreboard:
            scoreboard[f'{correct_guesser}'] += 1
        else:
            scoreboard[correct_guesser] = 1

        question, answer = choose_question(questions)
        correct_guesser = await self.handle_answers_round(interaction, question, answer)
        if correct_guesser in scoreboard:
            scoreboard[f'{correct_guesser}'] += 1
        else:
            scoreboard[correct_guesser] = 1

        #Sorts the scoreboard by points
        sorted_scoreboard = dict(sorted(scoreboard.items(),
                                  key=lambda item: item[1],
                                  reverse=True))

        await interaction.channel.send('Game Ended! Waiting for results')
        await asyncio.sleep(3)

        players = [f"`{i}`" for i in list(sorted_scoreboard.keys())]
        points = [f"{i}" for i in list(sorted_scoreboard.values())]

        embed = discord.Embed(title= f"Congratulations @{list(sorted_scoreboard.keys())[0]} !!\nﾠ",color=discord.Colour.blue())
        embed.set_author(name=f"We have a winner!\n",icon_url="https://cdn.discordapp.com/avatars/989409439956213830/8f7ddfeeb55e16b3afbf8b783d98b699.png?size=1024")
        embed.set_image(url="https://cdn.discordapp.com/attachments/989647128139808869/998440223052681306/Screenshot_3.png")
        embed.add_field(name="Scoreboard", value= '\n'.join(f"{players[o]}- **{points[o]}**" for o in range(len(players))),inline=False)

        await interaction.channel.send(embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(WordGame(client))