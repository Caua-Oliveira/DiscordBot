import discord
from discord import app_commands
from discord.ext import commands


#Used to remove players that found a match from the queue
def remove_matched_players(players, person):

    if person in players["top"]:
        players["top"].pop(players["top"].index(person))
    else:
        pass
    if person in players["jungle"]:
        players["jungle"].pop(players["jungle"].index(person))
    else:
        pass
    if person in players["mid"]:
        players["mid"].pop(players["mid"].index(person))
    else:
        pass
    if person in players["adc"]:
        players["adc"].pop(players["adc"].index(person))
    else:
        pass
    if person in players["sup"]:
        players["sup"].pop(players["sup"].index(person))
    else:
        pass

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


#Used when there are enough players to play a match
async def match_found(players, interaction: discord.Interaction):

    matched_players = {
        "top_blue":None,
        "jungle_blue":None,
        "mid_blue": None,
        "adc_blue": None,
        "sup_blue": None,
        "top_red":None,
        "jungle_red":None,
        "mid_red": None,
        "adc_red": None,
        "sup_red": None
    }

    matched_players["top_blue"] = '<:TOP:1002810797946318849>❔ ' + players["top"][0]
    remove_matched_players(players, players["top"][0])

    matched_players["jungle_blue"] = '<:JUNGLE:1002810786219053086>❔ ' + players["jungle"][0]
    remove_matched_players(players, players["jungle"][0])

    matched_players["mid_blue"] = '<:MID:1002810772151357500>❔ ' + players["mid"][0]
    remove_matched_players(players, players["mid"][0])

    matched_players["adc_blue"] = '<:ADC:1002810758419189851>❔ ' + players["adc"][0]
    remove_matched_players(players, players["adc"][0])

    matched_players["sup_blue"] = '<:SUP:1002810744825450537>❔ ' + players["sup"][0]
    remove_matched_players(players, players["sup"][0])

    matched_players["top_red"] = '<:TOP:1002810797946318849>❔ ' + players["top"][0]
    remove_matched_players(players, players["top"][0])

    matched_players["jungle_red"] = '<:JUNGLE:1002810786219053086>❔ ' + players["jungle"][0]
    remove_matched_players(players, players["jungle"][0])

    matched_players["mid_red"] = '<:MID:1002810772151357500>❔ ' + players["mid"][0]
    remove_matched_players(players, players["mid"][0])

    matched_players["adc_red"] = '<:ADC:1002810758419189851>❔ ' + players["adc"][0]
    remove_matched_players(players, players["adc"][0])

    matched_players["sup_red"] = '<:SUP:1002810744825450537>❔ ' + players["sup"][0]
    remove_matched_players(players, players["sup"][0])



    #embed
    match = discord.Embed(title='Match Found\nㅤ', colour=discord.Colour.green())
    match.add_field(name='Blue side', value=f'{matched_players["top_blue"]}\n{matched_players["jungle_blue"]}\n{matched_players["mid_blue"]}\n{matched_players["adc_blue"]}\n{matched_players["sup_blue"]}',
                        inline=True)
    match.add_field(name='Red side', value=f'{matched_players["top_red"]}\n{matched_players["jungle_red"]}\n{matched_players["mid_red"]}\n{matched_players["adc_red"]}\n{matched_players["sup_red"]}',
                        inline=True)
    await interaction.channel.send('||' + ','.join(x[x.index(' '):] for x in matched_players.values()) + '||', embed=match)
    await interaction.message.delete()
    roles = RolesButtons(players)
    await interaction.channel.send(embed=searching_match_embed(players), view=roles)


#Buttons that add users in a role
class RolesButtons(discord.ui.View):
    def __init__(self, players):
        super().__init__(timeout=500.0)
        self.players = players


    @discord.ui.button(emoji='<:TOP:1002810797946318849>', label= 'Top', style=discord.ButtonStyle.gray)
    async def top(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.mention not in self.players["top"]:
            self.players["top"].append(interaction.user.mention)
            if len(self.players["top"]) >= 2 and len(self.players["jungle"]) >= 2 and len(
                    self.players["mid"]) >= 2 and len(self.players["adc"]) >= 2 and len(self.players["sup"]) >= 2:
                await match_found(self.players, interaction)
                return interaction.response

            await interaction.message.delete()
            await interaction.channel.send(embed=searching_match_embed(self.players), view=self)



    @discord.ui.button(emoji='<:JUNGLE:1002810786219053086>', label= 'Jungle', style=discord.ButtonStyle.gray)
    async def jungle(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.mention not in self.players["jungle"]:
            self.players["jungle"].append(interaction.user.mention)
            if len(self.players["top"]) >= 2 and len(self.players["jungle"]) >= 2 and len(
                    self.players["mid"]) >= 2 and len(self.players["adc"]) >= 2 and len(self.players["sup"]) >= 2:
                await match_found(self.players, interaction)
                return interaction.response

            await interaction.message.delete()
            await interaction.channel.send(embed=searching_match_embed(self.players), view=self)


    @discord.ui.button(emoji='<:MID:1002810772151357500>', label= 'Mid', style=discord.ButtonStyle.gray)
    async def mid(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.mention not in self.players["mid"]:
            self.players["mid"].append(interaction.user.mention)
            if len(self.players["top"]) >= 2 and len(self.players["jungle"]) >= 2 and len(
                    self.players["mid"]) >= 2 and len(self.players["adc"]) >= 2 and len(self.players["sup"]) >= 2:
                await match_found(self.players, interaction)
                return interaction.response

            await interaction.message.delete()
            await interaction.channel.send(embed=searching_match_embed(self.players), view=self)

    @discord.ui.button(emoji='<:ADC:1002810758419189851>', label= 'Adc', style=discord.ButtonStyle.gray)
    async def adc(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.mention not in self.players["adc"]:
            self.players["adc"].append(interaction.user.mention)
            if len(self.players["top"]) >= 2 and len(self.players["jungle"]) >= 2 and len(
                    self.players["mid"]) >= 2 and len(self.players["adc"]) >= 2 and len(self.players["sup"]) >= 2:
                await match_found(self.players, interaction)
                return interaction.response

            await interaction.message.delete()
            await interaction.channel.send(embed=searching_match_embed(self.players), view=self)

    @discord.ui.button(emoji='<:SUP:1002810744825450537>', label= 'Sup', style=discord.ButtonStyle.gray)
    async def sup(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.mention not in self.players["sup"]:
            self.players["sup"].append(interaction.user.mention)
            if len(self.players["top"]) >= 2 and len(self.players["jungle"]) >= 2 and len(
                    self.players["mid"]) >= 2 and len(self.players["adc"]) >= 2 and len(self.players["sup"]) >= 2:
                await match_found(self.players, interaction)
                return interaction.response

            await interaction.message.delete()
            await interaction.channel.send(embed=searching_match_embed(self.players), view=self)


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
            "adc":["edu", "pietro"],
            "sup":["tiago", "gui"]
        }

        roles = RolesButtons(players)
        await interaction.channel.send(embed=searching_match_embed(players), view=roles)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Matchmaking(client))