import discord
from discord import app_commands
from discord.ext import commands


#Used to remove players that found a match from the queue
def remove_matched_players(players, person):
    for i in players:
        if person in players[i]:
            players[i].pop(players[i].index(person))


#Used to send the queue embed
def searching_match_embed(players):
    total = len(set(list(players["top"] + players["jungle"] + players["mid"] + players["adc"] + players["sup"])))
    embed = discord.Embed(title=f'Queue ({total} total players)', description=
    f'<:TOP:1002810797946318849> `({len(players["top"])})` ' + (', '.join(x for x in players["top"]) if len(players["top"]) > 0 else '') +
    f'\n<:JUNGLE:1002810786219053086> `({len(players["jungle"])})`' + (', '.join(x for x in players["jungle"]) if len(players["jungle"]) > 0 else '')+
    f'\n<:MID:1002810772151357500> `({len(players["mid"])})`' + (', '.join(x for x in players["mid"]) if len(players["mid"]) > 0 else '')+
    f'\n<:ADC:1002810758419189851> `({len(players["adc"])})`' + (', '.join(x for x in players["adc"]) if len(players["adc"]) > 0 else '')+
    f'\n<:SUP:1002810744825450537> `({len(players["sup"])})`' + (', '.join(x for x in players["sup"]) if len(players["sup"]) > 0 else ''))
    return embed


#Buttons to accept or deny the match
class AcceptMatch(discord.ui.View):
    def __init__(self, matched_players, interaction: discord.Interaction):
        super().__init__(timeout=10.0)
        self.response = None
        self.refused = False
        self.matched_players = matched_players

    #Cancels the match on timeout
    async def on_timeout(self) -> None:
        if not self.refused:
            match = discord.Embed(title='Timed Out ⚠', colour=discord.Colour.yellow())
            match.add_field(name='Blue side', value=f'{self.matched_players["top_blue"].replace("❔", "⚠")}\n{self.matched_players["jungle_blue"].replace("❔", "⚠")}\n{self.matched_players["mid_blue"].replace("❔", "⚠")}\n{self.matched_players["adc_blue"].replace("❔", "⚠")}\n{self.matched_players["sup_blue"].replace("❔", "⚠")}',
                            inline=True)
            match.add_field(name='Red side', value=f'{self.matched_players["top_red"].replace("❔", "⚠")}\n{self.matched_players["jungle_red"].replace("❔", "⚠")}\n{self.matched_players["mid_red"].replace("❔", "⚠")}\n{self.matched_players["adc_red"].replace("❔", "⚠")}\n{self.matched_players["sup_red"].replace("❔", "⚠")}',
                            inline=True)
            await self.response.edit(embed=match, view=None)
        else:
            return

    #Accept Button
    @discord.ui.button(label='Accept', style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        for i in self.matched_players:
            if interaction.user.mention in self.matched_players[i]:
                self.matched_players[i] = self.matched_players[i].replace("❔", "✅")
                break

        #Embed
        match = discord.Embed(title='Match Found\nㅤ', colour=discord.Colour.green())
        match.add_field(name='Blue side',
                        value=f'{self.matched_players["top_blue"]}\n{self.matched_players["jungle_blue"]}\n{self.matched_players["mid_blue"]}\n{self.matched_players["adc_blue"]}\n{self.matched_players["sup_blue"]}',
                        inline=True)
        match.add_field(name='Red side',
                        value=f'{self.matched_players["top_red"]}\n{self.matched_players["jungle_red"]}\n{self.matched_players["mid_red"]}\n{self.matched_players["adc_red"]}\n{self.matched_players["sup_red"]}',
                        inline=True)

        await interaction.response.edit_message(embed=match)


    #Refuse Button
    @discord.ui.button(label='Refuse', style=discord.ButtonStyle.red)
    async def refuse(self, interaction: discord.Interaction, button: discord.ui.Button):

        for i in self.matched_players:
            if interaction.user.mention in self.matched_players[i]:
                self.matched_players[i] = self.matched_players[i].replace("❔", "❌").replace("✅", "❌")
                break

        #Embed
        match = discord.Embed(title='Match Refused ❌', colour=discord.Colour.red())
        match.add_field(name='Blue side',
                        value=f'{self.matched_players["top_blue"]}\n{self.matched_players["jungle_blue"]}\n{self.matched_players["mid_blue"]}\n{self.matched_players["adc_blue"]}\n{self.matched_players["sup_blue"]}',
                        inline=True)
        match.add_field(name='Red side',
                        value=f'{self.matched_players["top_red"]}\n{self.matched_players["jungle_red"]}\n{self.matched_players["mid_red"]}\n{self.matched_players["adc_red"]}\n{self.matched_players["sup_red"]}',
                        inline=True)

        self.refused = True
        await self.response.edit(embed=match, view=None)


#Used when there are enough players to play a match
async def match_found(players, interaction: discord.Interaction):

    matched_players = {
        "top_blue" : None,
        "jungle_blue": None,
        "mid_blue": None,
        "adc_blue": None,
        "sup_blue": None,
        "top_red": None,
        "jungle_red": None,
        "mid_red": None,
        "adc_red": None,
        "sup_red": None
    }

    lanes = ["top", "jungle", "mid", "adc", "sup", "top", "jungle", "mid", "adc", "sup"]
    emotes = ['<:TOP:1002810797946318849>❔ ', '<:JUNGLE:1002810786219053086>❔ ', '<:MID:1002810772151357500>❔ ', '<:ADC:1002810758419189851>❔ ', '<:SUP:1002810744825450537>❔ ',
              '<:TOP:1002810797946318849>❔ ', '<:JUNGLE:1002810786219053086>❔ ', '<:MID:1002810772151357500>❔ ', '<:ADC:1002810758419189851>❔ ', '<:SUP:1002810744825450537>❔ ']

    for i in range(10):
        lane = lanes[i]
        key = list(matched_players.keys())[i]
        matched_players[key] = emotes[i] + players[lane][0]
        remove_matched_players(players, players[lane][0])

    #Embed
    match = discord.Embed(title='Match Found\nㅤ', colour=discord.Colour.green())
    match.add_field(name='Blue side', value=f'{matched_players["top_blue"]}\n{matched_players["jungle_blue"]}\n{matched_players["mid_blue"]}\n{matched_players["adc_blue"]}\n{matched_players["sup_blue"]}',
                        inline=True)
    match.add_field(name='Red side', value=f'{matched_players["top_red"]}\n{matched_players["jungle_red"]}\n{matched_players["mid_red"]}\n{matched_players["adc_red"]}\n{matched_players["sup_red"]}',
                        inline=True)


    accept = AcceptMatch(matched_players, interaction)
    out = await interaction.channel.send('||' + ','.join(x[x.index(' '):] for x in matched_players.values()) + '||', embed=match, view = accept)
    accept.response = out


#Used to add players to the queue
async def add_to_queue(players, lane, interaction: discord.Interaction):
    players[lane].append(interaction.user.mention)
    if len(players["top"]) >= 2 and len(players["jungle"]) >= 2 and len(
            players["mid"]) >= 2 and len(players["adc"]) >= 2 and len(players["sup"]) >= 2:
        await match_found(players, interaction)

    #Deletes previous queue message and updates it
    await interaction.message.delete()
    await interaction.channel.send(embed=searching_match_embed(players), view=RolesButtons(players))

#Buttons to choose your role
class RolesButtons(discord.ui.View):
    def __init__(self, players):
        super().__init__(timeout=500.0)
        self.players = players


    #Top Button
    @discord.ui.button(emoji='<:TOP:1002810797946318849>', label= 'Top', style=discord.ButtonStyle.gray)
    async def top(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.mention not in self.players["top"]:
            await add_to_queue(self.players, "top", interaction)


    #Jungle Button
    @discord.ui.button(emoji='<:JUNGLE:1002810786219053086>', label= 'Jungle', style=discord.ButtonStyle.gray)
    async def jungle(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.mention not in self.players["jungle"]:
            await add_to_queue(self.players, "jungle", interaction)


    #Mid Button
    @discord.ui.button(emoji='<:MID:1002810772151357500>', label= 'Mid', style=discord.ButtonStyle.gray)
    async def mid(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.mention not in self.players["mid"]:
            await add_to_queue(self.players, "mid", interaction)


    #Adc Button
    @discord.ui.button(emoji='<:ADC:1002810758419189851>', label= 'Adc', style=discord.ButtonStyle.gray)
    async def adc(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.mention not in self.players["adc"]:
            await add_to_queue(self.players, "adc", interaction)


    #Sup Button
    @discord.ui.button(emoji='<:SUP:1002810744825450537>', label= 'Sup', style=discord.ButtonStyle.gray)
    async def sup(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.mention not in self.players["sup"]:
            await add_to_queue(self.players, "sup", interaction)


#The command root
class Matchmaking(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name='matchmaking')
    async def matchmaking(self, interaction: discord.Interaction):
        await interaction.response.send_message('The command started!', ephemeral=True)

        players = {
            "top":["joao"],
            "jungle":["pedro", "lucio", "luan"],
            "mid":["carla", "joaquin"],
            "adc":["edu", "carl"],
            "sup":["tiago", "gui"]
        }

        await interaction.channel.send(embed=searching_match_embed(players),view=RolesButtons(players))

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Matchmaking(client))