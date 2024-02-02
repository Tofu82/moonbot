#Imports
import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio
import rolimons

TOKEN = 'REPLACE WITH DISCORD BOTS TOKEN'

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True

bot= commands.Bot(command_prefix="!", intents = intents)

#Check logged in
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print (f"Synced {len(synced)} commands(s)")
    except Exception as e:
        print (e)

import discord
from discord.ext import commands

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
    # Send the embed message
    await ctx.send(embed=embed)

#Help Command
@bot.tree.command(name="help")
async def help(interaction: discord.Interaction):
    embed=discord.Embed(title= "Help", colour= discord.Colour.blurple())
    embed.add_field(name= "/user", value= "Checks users RAP and value")
    embed.add_field(name="/value", value= "Checks users value")
    embed.add_field(name="/rap", value= "Checks users RAP")
    embed.add_field(name="/help", value ="Displays this help command ")
    embed.add_field(name="!purge (amount)", value ="Purges chat of (amount) messages")
    await interaction.response.send_message(embed=embed)

#Checks inputted roblox usernames Value
@bot.tree.command(name="value", )
@app_commands.describe(player_name = "Player Name:")
async def uservalue(interaction: discord.Interaction, player_name: str):
    try:
        player = rolimons.player (name = player_name )
        if int(player.value) >0:
            embed=discord.Embed(title= player_name, colour=discord.Colour.blurple())
            embed.add_field(name= "**Value**", value= f"{player.value:,}<:bobux:1191956397756272700>")
            await interaction.response.send_message(embed=embed)
        else:
            embed=discord.Embed(title= "An error occured (player value = 0)", colour= discord.Colour.red())
            embed.add_field(name= "__**What is this error caused by?:**__", value= "This error is usually caused by:\n- The player's inventory is private\n- The player is banned") 
            await interaction.response.send_message(embed=embed)
    except Exception as e:
            embed=discord.Embed(title= "Player does not exist", colour= discord.Colour.red())
            embed.add_field(name= "__**Player does not exist**__", value = "An error occured:\n - Player does not exist")
            await interaction.response.send_message(embed=embed)

#Checks inputted roblox usernames RAP
@bot.tree.command(name="rap")
@app_commands.describe(player_name = "Player Name:")
async def userrap(interaction: discord.Interaction, player_name: str):
    try:
         player = rolimons.player (name = player_name )
         if int(player.rap) > 0:
            embed=discord.Embed(title= player_name, colour=discord.Colour.blurple())
            embed.add_field(name= "**RAP**", value= f"{player.rap:,}<:bobux:1191956397756272700>")
            await interaction.response.send_message(embed=embed)
         else:
            embed=discord.Embed(title= "An error occured (player RAP = 0)", colour= discord.Colour.red())
            embed.add_field(name= "__**What is this error caused by?:**__", value= "This error is usually caused by:\n- The player's inventory is private\n- The player is banned")
            await interaction.response.send_message(embed=embed)
    except Exception as e:
            embed=discord.Embed(title= "Player does not exist", colour= discord.Colour.red())
            embed.add_field(name= "__**Player does not exist**__", value = "An error occured:\n - Player does not exist")
            await interaction.response.send_message(embed=embed)

#Checks inputted roblox usernames RAP + Value
@bot.tree.command(name="user")
@app_commands.describe(player_name = "Player Name:")
async def user(interaction: discord.Interaction, player_name: str):
    try:
        player = rolimons.player (name = player_name )
        if int(player.rap) and int(player.value) >0:
            embed=discord.Embed(title= player_name, colour=discord.Colour.blurple())
            embed.add_field(name= "**Value**", value= f"{player.value:,}<:bobux:1191956397756272700>")
            embed.add_field(name= "**RAP**", value= f"{player.rap:,}<:bobux:1191956397756272700>")
            await interaction.response.send_message(embed=embed)
        else:
            embed=discord.Embed(title= "An error occured (player value and RAP = 0)", colour= discord.Colour.red())
            embed.add_field(name= "__**What is this error caused by?:**__", value= "This error is usually caused by:\n- The player's inventory is private\n- The player is banned")
            await interaction.response.send_message(embed=embed)
    except Exception as e:
            embed=discord.Embed(title= "Player does not exist", colour= discord.Colour.red())
            embed.add_field(name= "__**Player does not exist**__", value = "An error occured:\n - Player does not exist")
            await interaction.response.send_message(embed=embed)
bot.run(TOKEN)
