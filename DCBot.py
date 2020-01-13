import discord
from discord.ext import commands, tasks
from itertools import cycle

bot = commands.Bot(command_prefix='/teapot ')
status = cycle(['/TeaPot ', 'redtea.red'])


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('/teapot | redtea.red'))
    print("Bot is Online.")


@bot.event
async def on_member_join(member):
    print(f'{member} has joined a server.')


@bot.event
async def on_member_remove(member):
    print(f'{member} has leaved a server.')


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)} ms')  # ping


@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        await ctx.send(f'{member} has been kicked!')
        print(f'{member} has been kicked!')
    except Exception as failban:
        await ctx.send("Failed to ban: Missing Permissions ")


@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f'{member} has been Banned!')
        print(f'{member} has been Banned!')
    except Exception as failban:
        await ctx.send("Failed to ban: Missing Permissions ")


@bot.command()
async def ver(ctx):
    await ctx.send(" By RedTea | GitHub: https://github.com/lRedTeal/TeaPot ")
    await ctx.send(" Code w Python >3 with Discord.py ")


@bot.command()
async def admin(ctx):
    await ctx.send("You don't have permission to perform this command!")


@tasks.loop(seconds=10)
async def status():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(next(status)))


try:
    from configparser import ConfigParser

    parser = ConfigParser()
    parser.read('Config.ini')
    token = parser.get('Main', 'Token')
    bot.run(token)
except Exception as loginFail:
    print("Error:Login fail, please check the Token! Make Sure you have Run Setup.py once time!")

# Gittest
