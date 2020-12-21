import discord
from discord.ext import commands
from main import col, owner, notification_channel
from time import time
from random import choice


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = self.bot.get_channel(690907452023242752)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('...'))
        print("Ready")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel:
            ban = col.find_one({"_id": member.id})["ban_time"]
            if ban and int(time()) < ban:
                print(type(self.channel))
                await member.move_to(None)
                await self.channel.send(
                    f"__{member.display_name}__ всё ещё на хуе. Ему осталось **{round(ban - int(time()))}** секунд")
            elif ban is not None:
                col.update_one({"_id": member.id}, {"$set": {"ban_time": None}})

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(690908836391026728)
        role = discord.utils.get(member.guild.roles, id=681396936011808791)
        welcome_msg = ["залетел в бомжатник"]
        await member.add_roles(role)
        await channel.send(f"{member.mention} {choice(welcome_msg)}")
        col.insert_one({
            "_id": member.id,
            "name": member.display_name,
            "level": 1,
            "ban_time": None,
        })

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error_channel = self.bot.get_channel(683559787203788896)
        await error_channel.send(f'{ctx.author.mention} caused "{error}"')
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Шо за хуйню ты написал? Нет такой команды')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Ты где-то проебался с цифрами')


def setup(bot):
    bot.add_cog(Events(bot))
