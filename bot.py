import asyncio
import discord
import os

from discord.ext import commands, tasks 

from Help import CustomHelpCommand
from admincheck import admin_check

# Intents
intents = discord.Intents.all()

client = commands.Bot(command_prefix="!", help_command=CustomHelpCommand(), case_insensitive=True, intents=intents)
client.mute_message = None
status = "Design Project"

@client.event
async def on_ready():
    print('Bot = ready')

#Loads extension
@client.command()
@commands.check(admin_check)
async def load(ctx, extension):
    await client.load_extension(f'cogs.{extension}')
    await ctx.send("Succesfully loaded `" + extension + '`')

#Unloads extension
@client.command()
@commands.check(admin_check)
async def unload(ctx, extension):
    await client.unload_extension(f'cogs.{extension}')
    await ctx.send("Succesfully unloaded `" + extension + '`')

#Reloads extension
@client.command()
@commands.check(admin_check)
async def reload(ctx, extension):
    await client.unload_extension(f'cogs.{extension}')
    await client.load_extension(f'cogs.{extension}')
    await ctx.send("Succesfully reloaded `" + extension + '`')

#Loads every extensions in cogs
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')

async def main():
    with open('token.txt', 'r') as file:
        token = file.readline()
        print("Reading token...")
    await load_extensions()
    await client.start(token)

asyncio.run(main())