from discord.ext import commands
import discord
from main import col, owner, notification_channel


class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def auth(self, ctx):
        if ctx.author.id == owner:
            data = []
            for member in ctx.guild.members:
                if col.count_documents({"_id": member.id}) == 0:
                    data.append({
                        "_id": member.id,
                        "name": member.display_name,
                        "level": 3,
                        "ban_time": None,
                    })
            col.insert_many(data)

    @commands.command()
    @commands.is_owner()
    async def lvlup(self, ctx, member: discord.Member = None):
        level = 1
        member = member or ctx.author
        prev_lvl = col.find_one({"_id": member.id})["level"]
        if 5 > prev_lvl > 1:
            col.update_one({"_id": member.id}, {"$inc": {"level": level}})
            await ctx.send(f"Уровень {member.mention} изменен с {prev_lvl} на {prev_lvl + level}")
        else:
            if prev_lvl >= 5:
                await ctx.send("У него итак максимальный лвл. Куда больше то?")
            else:
                await ctx.send("Ты ебанулся? Куда меньше то")

    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        lvl = col.find_one({"_id": member.id})["level"]
        await ctx.send(f"У тебя __{lvl}__ уровень")

























def setup(bot):
    bot.add_cog(Levels(bot))
