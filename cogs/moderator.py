from discord.ext import commands
import discord
from main import col, owner, notification_channel
from time import time
from random import randint


class Moder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx, member: discord.Member):
        if col.find_one({"_id": ctx.author.id}) == 5:
            await member.ban()
            await ctx.send(f"Петушара {member.mention} отлетел в бан")
        else:
            await ctx.send("Недорос ещё стручок для такого")

    @commands.command()
    async def nahui(self, ctx, member: discord.Member, duration=5):
        if col.find_one({"_id": ctx.author.id})['level'] < 5:
            await ctx.send("Малой ещё")
        else:
            ban_time = time() + duration
            col.update_one({"_id": member.id}, {"$set": {"ban_time": ban_time}})
            await member.move_to(None)
            await ctx.send(f"{member.display_name} был послан нахуй на **{duration}** секунд")

    @commands.command()
    async def stop(self, ctx, member:discord.Member):
        col.update_one({"_id": member.id}, {"$set": {"ban_time": None}})
        await ctx.send(f"Великодушный барин __{ctx.author.display_name}__ снял холопа {member.mention} с хуя за хорошее поведение")

    @commands.command()
    async def clear(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount + 1)
        channel = self.bot.get_channel(681414780351021090)
        await channel.send(f'{ctx.author.name} Очистил {amount} сообщений')

    @commands.command()
    async def kick(self, ctx, member: discord.Member):
        if col.find_one({"_id": ctx.author.id})["level"] < 4:
            await ctx.send("Хуй тебе")
            return 0
        if col.find_one({"_id": member.id})["level"] >= 4:
            await ctx.send('Неа, хуй там плавал')
        else:
            await member.kick()
            channel = self.bot.get_channel(681414780351021090)
            await ctx.send(f'{ctx.author} выпнул бомжа {member.mention}')
            await channel.send(f'{ctx.author.mention} kicked {member.mention}')

    @commands.command()
    async def ban(self, ctx, member: discord.Member, reason='За кривой базар'):
        if col.find_one({"_id": ctx.author.id})["level"] < 5:
            await ctx.send("Хуй тебе")
            return 0
        if col.find_one({"_id": ctx.author.id})["level"] >= 5:
            await ctx.send('Неа, хуй там плавал')
        else:
            channel = self.bot.get_channel(681414780351021090)
            await member.ban(reason=reason)
            await ctx.send(f'{ctx.author.mention} закрыл доступ в петушатню {member.mention} {reason}')
            await channel.send(f'{ctx.author.mention} has banned {member.mention} for {reason}')


def setup(bot):
    bot.add_cog(Moder(bot))
