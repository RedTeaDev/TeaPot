from datetime import datetime
import discord
from discord.ext import commands, tasks
from itertools import cycle
import logging
from discord.ext import commands
from redtea import redtea
import time

# noinspection PyArgumentList
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s | %(name)-5s  | %(levelname)-8s | Thread: %(thread)-5s | %(message)s',
                    datefmt='[%m-%d %H:%M]',
                    handlers=[
                        logging.FileHandler(
                            'logs/bot.log'.format(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')), 'w',
                            'utf-8'), ])
# defind logger
print_debug = logging.debug
print_info = logging.info
print_warning = logging.warning
print_error = logging.error
print_critical = logging.critical

bot = commands.Bot(command_prefix='/teapot ')
status = cycle(['/TeaPot ', 'redtea.red'])


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('/teapot | redtea.red'))
    print("Bot is Online.")


@bot.event
async def on_member_join(member):
    print(f'{member} joined the server.')
    print(f'{member} joined the server.')


@bot.event
async def on_member_remove(member):
    print(f'{member} left the server.')
    print_info(f'{member} left the server.')


@bot.event
async def on_message(message):
    print_debug(f'{message}')


@bot.event
async def on_message(message):
    guild = message.guild
    if guild:
        path = "logs/{}.txt".format(guild.id)
        with open(path, 'a+') as f:
            print("{0.author.name} : {0.content}".format(message), file=f)
    await bot.process_commands(message)


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
    except Exception as failkick:
        await ctx.send("Failed to ban:" + str(failkick))


@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f'{member} has been Banned!')
        print(f'{member} has been Banned!')
    except Exception as failban:
        await ctx.send("Failed to ban:" + str(failban))


@bot.command()
async def ver(ctx):
    await ctx.send(" By RedTea | GitHub: https://github.com/lRedTeal/TeaPot ")
    await ctx.send(" Code w Python >3 with Discord.py API ")
    await ctx.send(" Build-03_DEBUG | RedTeaPackage: 0.3 | https://Forum.redtea.red")


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
