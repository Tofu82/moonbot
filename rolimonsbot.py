#Imports
import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio
import rolimons
import os

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True

bot= commands.Bot(command_prefix="!", intents = intents)
token = 'REPLACE_WITH_YOUR_TOKEN'

#Check logged in
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print (f"Synced {len(synced)} commands(s)")
    except Exception as e:
        print (e)

client = commands.Bot(command_prefix='/', intents=discord.Intents.all())

#Purge Command
@commands.has_permissions(manage_messages=True)
@bot.command(name='purge', brief='Deletes a specified number of messages from the current channel')
async def purge(ctx, amount: int):
  # Delete the specified number of messages
  deleted = await ctx.channel.purge(limit=amount)
  if len(deleted) == 0:
    # If no messages were deleted, create an embed message with a custom color and text
    embed = discord.Embed(title='Purge complete', color= discord.Colour.blurple())
    embed.description = 'No messages were deleted'
    # Set the user's profile picture as the thumbnail of the embed
    embed.set_thumbnail(url=ctx.author.avatar.url)
    # Send the embed message
    await ctx.send(embed=embed)
  else:
    # Create an embed message with a custom color and text
    embed = discord.Embed(title='Purge complete', colour =discord.Colour.blurple())
    if len(deleted) == 1:
      # If only one message was deleted, use singular text
      embed.description = '1 message was deleted'
    else:
      # If more than one message was deleted, use plural text
      embed.description = f'{len(deleted)} messages were deleted'
    # Set the user's profile picture as the thumbnail of the embed
    embed.set_thumbnail(url=ctx.author.avatar.url)
    #Set moonbot author 
    embed.set_author(name="Moonbot", url=("https://github.com/Tofu42O/rolimonsbot"), icon_url=("https://upload.wikimedia.org/wikipedia/commons/b/b8/Moon_rotating_full_160px.gif"))
    # Send the embed message
    await ctx.send(embed=embed)

#Help Command
@bot.tree.command(name="help", description= "Help command")
async def help(interaction: discord.Interaction):
    embed=discord.Embed(title= "Help", colour= discord.Colour.blurple())
    embed.set_author(name="Moonbot", url=("https://github.com/Tofu42O/rolimonsbot"), icon_url=("https://upload.wikimedia.org/wikipedia/commons/b/b8/Moon_rotating_full_160px.gif"))
    embed.add_field(name= "/user", value= "Checks users RAP and value")
    embed.add_field(name="/value", value= "Checks users value")
    embed.add_field(name="/rap", value= "Checks users RAP")
    embed.add_field(name="/item", value= "Checks the value and RAP of a specific item")
    embed.add_field(name="/leaderboard", value ="Displays the leaderboard")
    embed.add_field(name="!purge (amount)", value ="Purges chat of (amount) messages")
    await interaction.response.send_message(embed=embed)

#Checks inputted roblox usernames Value
@bot.tree.command(name="value", description= "Checks users value")
@app_commands.describe(player_name = "Player Name:")
async def uservalue(interaction: discord.Interaction, player_name: str):
    try:
        player = rolimons.player (name = player_name)
        if rolimons.exceptions.PlayerNotFound:
            embed=discord.Embed(title= "Player does not exist", colour= discord.Colour.red())
            embed.add_field(name= "__**Player does not exist**__", value = "An error occured:\n - Player does not exist")
        if int(player.value) >0:
            url = f"https://www.roblox.com/users/{player.id}/profile"
            embed=discord.Embed(title=(player_name), url =(url), colour=discord.Colour.blurple())
            embed.set_author(name="Moonbot", url=("https://github.com/Tofu42O/rolimonsbot"), icon_url=("https://upload.wikimedia.org/wikipedia/commons/b/b8/Moon_rotating_full_160px.gif"))
            embed.add_field(name= "**Value**", value= f"{player.value:,}<:bobux:1191956397756272700>")
            await interaction.response.send_message(embed=embed)
        else:
            embed=discord.Embed(title= "An error occured (player value = 0)", colour= discord.Colour.red())
            embed.add_field(name= "__**What is this error caused by?:**__", value= "This error is usually caused by:\n- The player's inventory is private\n- The player is banned")
            if player.terminated:
              embed.add_field(name="⚠️", value= "**Player is terminated**", inline = False)
            await interaction.response.send_message(embed=embed)
    except Exception as e:
            embed=discord.Embed(title= "Player does not exist", colour= discord.Colour.red())
            embed.add_field(name= "__**Player does not exist**__", value = "An error occured:\n - Player does not exist")
            await interaction.response.send_message(embed=embed)

#Checks inputted roblox usernames RAP
@bot.tree.command(name="rap", description= "Checks users RAP")
@app_commands.describe(player_name = "Player Name:")
async def userrap(interaction: discord.Interaction, player_name: str):
    try:
         player = rolimons.player (name = player_name )
         if int(player.rap) >0:
            url = f"https://www.roblox.com/users/{player.id}/profile"
            embed=discord.Embed(title=(player_name), url =(url), colour=discord.Colour.blurple())
            embed.set_author(name="Moonbot", url=("https://github.com/Tofu42O/rolimonsbot"), icon_url=("https://upload.wikimedia.org/wikipedia/commons/b/b8/Moon_rotating_full_160px.gif"))
            embed.add_field(name= "**RAP**", value= f"{player.rap:,}<:bobux:1191956397756272700>")
            await interaction.response.send_message(embed=embed)
         else:
            embed=discord.Embed(title= "An error occured (player RAP = 0)", colour= discord.Colour.red())
            embed.add_field(name= "__**What is this error caused by?:**__", value= "This error is usually caused by:\n- The player's inventory is private\n- The player is banned")
            if player.terminated:
              embed.add_field(name="⚠️", value= "**Player is terminated**", inline = False)
            await interaction.response.send_message(embed=embed)
    except Exception as e:
            embed=discord.Embed(title= "Player does not exist", colour= discord.Colour.red())
            embed.add_field(name= "__**Player does not exist**__", value = "An error occured:\n - Player does not exist")
            await interaction.response.send_message(embed=embed)

#Checks inputted roblox usernames RAP + Value
@bot.tree.command(name="user", description= "Checks users RAP, value and rank")
@app_commands.describe(player_name = "Player Name:")
async def user(interaction: discord.Interaction, player_name: str):
    try:
        player = rolimons.player (name = player_name)
        if int(player.rap) >0 and int(player.value) >0:
            url = f"https://www.rolimons.com/player/{player.id}"
            embed=discord.Embed(title=(player_name), url =(url), colour=discord.Colour.blurple())
            embed.set_author(name="Moonbot", url=("https://github.com/Tofu42O/rolimonsbot"), icon_url=("https://upload.wikimedia.org/wikipedia/commons/b/b8/Moon_rotating_full_160px.gif"))
            embed.add_field(name= "**Value**", value= f"{player.value:,}<:bobux:1191956397756272700>")
            embed.add_field(name= "**RAP**", value= f"{player.rap:,}<:bobux:1191956397756272700>")
            if player.rank is not None and str(player.rank).lower() != "none":
              embed.add_field(name= "**Rank**", value= f"🎖️{player.rank}")
            await interaction.response.send_message(embed=embed)
        else:
            embed=discord.Embed(title= "An error occured (player value and RAP = 0)", colour= discord.Colour.red())
            embed.add_field(name= "__**What is this error caused by?:**__", value= "This error is usually caused by:\n- The player's inventory is private\n- The player is banned")
            if player.terminated:
              embed.add_field(name="⚠️", value= "**Player is terminated**", inline = False)
            await interaction.response.send_message(embed=embed)
    except Exception as e:
            embed=discord.Embed(title= "Player does not exist", colour= discord.Colour.red())
            embed.add_field(name= "__**Player does not exist**__", value = "An error occured:\n - Player does not exist")
            await interaction.response.send_message(embed=embed)

#Check items RAP and value
@bot.tree.command(name="item", description= "Checks items RAP and value")
@app_commands.describe(item_id = "Item id:")
async def itemchecker(interaction: discord.Interaction, item_id: int):
  try:
    item = rolimons.item(item_id)
    if item.value <= 0:
      embed=discord.Embed(title= "An error occured (item value = 0)", colour= discord.Colour.blurple())
      embed.add_field(name= "__**What is this error caused by?:**__", value= "This error is usually caused by:\n- The item doesn't exist\n- The item ID is invalid")
      await interaction.response.send_message(embed=embed)
    else:
      url = f"https://www.rolimons.com/item/{item.id}"
      embed=discord.Embed(title= f"{item.name} ({item.acronym})",url=(url) , colour= discord.Colour.blurple())
      embed.set_author(name="Moonbot", url=("https://github.com/Tofu42O/rolimonsbot"), icon_url=("https://upload.wikimedia.org/wikipedia/commons/b/b8/Moon_rotating_full_160px.gif"))
      embed.add_field(name= "**Value**", value= f"{item.value:,}<:bobux:1191956397756272700>", inline = True)
      embed.add_field(name= "**RAP**", value= f"{item.rap:,}<:bobux:1191956397756272700>", inline = True)
      print(item.trend)
      if item.projected:
        embed.add_field(name= "⚠️", value="**Projected**", inline= False)
      if item.rare:
          embed.add_field(name= "💎", value="**Rare**", inline= False)
      await interaction.response.send_message(embed=embed)
  except Exception as e:
    embed=discord.Embed(title= "An error occured", colour= discord.Colour.red())
    embed.add_field(name= "__**This error could be caused by:**__", value = "- The item doesn't exist\n- The item isn't a limited")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="leaderboard", description= "Displays the leaderboard")
async def leaderboard(interaction: discord.Interaction):
    utils_instance = rolimons.utils()
    players = utils_instance.get_leaderboard()
    top_10_players = players[:10]

    embed=discord.Embed(title="**Leaderboard**", url=("https://www.rolimons.com/leaderboard"), colour= discord.Colour.blurple())
    embed.set_author(name="Moonbot", url=("https://github.com/Tofu42O/rolimonsbot"), icon_url=("https://upload.wikimedia.org/wikipedia/commons/b/b8/Moon_rotating_full_160px.gif"))
    for player in top_10_players:
      embed.add_field(name=f"{player.rank}. {player.name}", 
                      value=f"**Value:** {player.value}<:bobux:1191956397756272700>  **RAP:** {player.rap}<:bobux:1191956397756272700>", inline = False
                     )
    await interaction.response.send_message(embed=embed)
bot.run(token)