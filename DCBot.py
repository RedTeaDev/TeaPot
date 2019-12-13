import discord
from discord.ext import commands, tasks
from itertools import cycle

bot = commands.Bot(command_prefix='/teapot ')
status = cycle(['/TeaPot ', 'redtea.red'])


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game('Starting..'))
    print("Bot is ready.")


@bot.event
async def on_member_join(member):
    print(f'{member} has joined a server.')


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)} ms') #ping

@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@bot.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member} has been kicked!')

@bot.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f'{member} has been Banned!')
    except Exception as failban:
        await ctx.send("Fail to ban: Missing Permissions ")

@tasks.loop(seconds=10)
async def status():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(next(status)))

try:
    bot.run('replace_here')
except Exception as loginFail:
    print("Error:Login fail, please check the Token!")
