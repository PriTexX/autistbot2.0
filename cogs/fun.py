import discord
from discord.ext import commands
from main import col, owner, notification_channel
from random import randint, choice
import re
import time
import json
import asyncio


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bibametr(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        bibaless = [1,2]
        if member.id in bibaless:
            await ctx.send(f"У {member.mention} нет бибы. Он лох")
            return 0
        msg_big = [
            "Мне бы такого парня с **{1}** см, как у {0}",
            "У {0} настолько большой хуй, что он может кого-нибудь поколечить им (**{1}**)",
            "У {0} хуй как Эйфелевая башня **{1}**",
        ]
        msg_medium = [
            "По статистическим данным хуй {0} больше, чем у азиата **{1}**",
            "У {0} целых **{1}** см он может гордиться собой",
            "У {0} обычный хуй **{1}** см, ничего удивительно",
        ]
        msg_small = [
            "'Уиу, уиу' у {0} маленький пиструн **{1}** см ему срочно нужна операция",
            "У {0} маленькая биба **{1}** см",
            "У {0} **{1}** см. В комнате просто холодно",
        ]
        if member.id == 307785148852862978:
            size = randint(1, 5)
        else:
            size = randint(1, 30)
        if size >= 23:
            await ctx.send(choice(msg_big).format(member.mention, size))
        elif size >= 15:
            await ctx.send(choice(msg_medium).format(member.mention, size))
        else:
            await ctx.send(choice(msg_small).format(member.mention, size))
            korotkostvol = randint(5, 30)
            await ctx.send(f"За маленькую бибу {member.mention} отправляется к короткостволам на {korotkostvol} сек")
            role = discord.utils.get(ctx.author.guild.roles, id=703583464653324328)
            await member.add_roles(role)
            await asyncio.sleep(korotkostvol)
            await ctx.send(f"{member.mention} был освобожден из короткостволов")
            await member.remove_roles(role)

    @commands.command()
    async def spam(self, ctx, member: discord.Member, *shit):
        obj = re.search("\s{0,}\d{1,}\s{0,}", shit)
        amount = int(obj[0])
        msg = shit[0:obj.start()] + " " + shit[obj.end():]
        if amount > 200:
            await ctx.send("Дохуя спама")
            return 0
        if col.find_one({"_id": ctx.author.id})["level"] < 4:
            await ctx.send("Хуй тебе")
        else:
            for i in range(amount):
                await member.send(str(msg))
                time.sleep(0.1)


    @commands.command()
    async def petuh(self, ctx, member: discord.Member):
        if col.find_one({"_id": ctx.author.id})["level"] > 4:
            with open(r'cogs\data_file2.json', 'r') as file:
                TakenRoles = json.load(file)
            roles_to_take = [role.name for role in member.roles]
            TakenRoles[member.name] = roles_to_take
            with open(r'cogs/data_file2.json', 'w') as file:
                json.dump(TakenRoles, file)
            mute_role = discord.utils.get(ctx.message.guild.roles, name='петушарня')
            await member.add_roles(mute_role)
            for i in range(1, len(roles_to_take)):
                await member.remove_roles(discord.utils.get(ctx.message.guild.roles, name=roles_to_take[i]))
            await member.move_to(self.bot.get_channel(681777814995075075))
            await ctx.send(f'{member.mention} был лишен всех прав и отправлен в ПЕТУШАРНЮ')
        else:
            await ctx.send(f"Недорос петушок ещё, чтобы других в петушарню отправлять")

    @commands.command()
    async def unpetuh(self, ctx, member: discord.Member):
        if col.find_one({"_id": ctx.author.id})["level"] < 5:
            return 0
        with open(r'cogs/data_file2.json', 'r') as file:
            TakenRoles = json.load(file)
        remove_role = discord.utils.get(ctx.message.guild.roles, name='петушарня')
        await member.remove_roles(remove_role)
        roles_to_give = TakenRoles[member.name]
        for role in range(1, len(roles_to_give)):
            await member.add_roles(discord.utils.get(ctx.message.guild.roles, name=roles_to_give[role]))
        await ctx.send(f'{ctx.author.mention} вытащил {member.mention} из ПЕТУШАТНИ и вернул все права')


def setup(bot):
    bot.add_cog(Fun(bot))
