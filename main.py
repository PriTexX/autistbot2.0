import discord
from discord.ext import commands
import os
from pymongo import MongoClient

password = os.environ.get("password")
s = "mongodb+srv://pritexx:{}@autistbot.stvuk.mongodb.net/dsusers?retryWrites=true&w=majority"
cluster = MongoClient(s.format(password))
col = cluster.dsusers.levels
owner = 229033111197843456
notification_channel = 681414780351021090

intents = discord.Intents.default()
intents.emojis = False
intents.integrations = False
intents.webhooks = False
intents.dm_reactions = False
intents.guild_reactions = False
intents.presences = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command()
async def load(ctx, extensions):
    bot.load_extension(f"cogs.{extensions}")
    await ctx.author.send("Done")


@bot.command()
async def unload(ctx, extensions):
    bot.unload_extension(f"cogs.{extensions}")
    await ctx.author.send("Done")


@bot.command()
async def reload(ctx, extensions):
    bot.unload_extension(f"cogs.{extensions}")
    bot.load_extension(f"cogs.{extensions}")
    await ctx.author.send("Done")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

        
TOKEN = os.eviron.get("TOKEN")

bot.run(TOKEN)
