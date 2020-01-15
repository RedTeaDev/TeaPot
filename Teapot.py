import logging
import os
import shutil
from configparser import ConfigParser
from datetime import datetime

import discord
import mysql.connector
import youtube_dl
from discord.ext import commands
from discord.utils import get

from redtea import redtea

print("""
  _____                      _   
 |_   _|__  __ _ _ __   ___ | |_ 
   | |/ _ \/ _` | '_ \ / _ \| __|
   | |  __/ (_| | |_) | (_) | |_ 
   |_|\___|\__,_| .__/ \___/ \__|
      by RedTea |_| & ColaIan
""")

# Check if config exists
if not os.path.isfile('config.ini'):
    print("Unable to find configuration file (config.ini). Running setup.py...")
    os.system("python setup.py")
    quit()

# Read config from config.ini
try:
    config = ConfigParser()
    config.read('config.ini')
    bot_token = config.get('Main', 'token')
    storage_type = config.get('Main', 'storage_type')
    if storage_type == "mysql":
        db_host = config.get('MySQL', 'host')
        db_database = config.get('MySQL', 'database')
        db_user = config.get('MySQL', 'user')
        db_password = config.get('MySQL', 'password')
    else:
        storage_type = "flatfile"
except Exception:
    print("Configuration error. Please check your configuration file!")
    quit()

if storage_type == "mysql":
    try:
        database = mysql.connector.connect(
            host=db_host,
            database=db_database,
            user=db_user,
            passwd=db_password
        )
        db = database.cursor(buffered=True)
        print(database)
    except Exception as error:
        print("\nUnable to connect to database. Aborting startup...\n" + str(error))
        quit()
    db.execute('CREATE TABLE IF NOT EXISTS `guilds` (`guild_id` BIGINT, `guild_name` TINYTEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS `channels` (`channel_id` BIGINT, `channel_name` TINYTEXT)')
    db.execute("CREATE TABLE IF NOT EXISTS `users` (`user_id` BIGINT, `user_name` TINYTEXT, `user_discriminator` INT)")

# Logger Configuration
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s | %(name)-5s  | %(levelname)-8s | Thread: %(thread)-5s | %(message)s',
                    datefmt='[%m-%d %H:%M]',
                    handlers=[
                        logging.FileHandler(
                            'logs/bot.log'.format(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')), 'w',
                            'utf-8'), ])

# define logger
print_debug = logging.debug
print_info = logging.info
print_warning = logging.warning
print_error = logging.error
print_critical = logging.critical

bot = commands.Bot(command_prefix='/teapot ')


# status = cycle(['/teapot ', 'redtea.red'])    [Not working]


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('/teapot help | redtea.red'))
    if storage_type == "mysql":
        for guild in bot.guilds:
            db.execute("SELECT * FROM `guilds` WHERE guild_id = '" + str(guild.id) + "'")
            if db.rowcount == 0:
                db.execute("INSERT INTO `guilds`(guild_id, guild_name) VALUES(%s, %s)", (guild.id, guild.name))
                database.commit()
            db.execute("CREATE TABLE IF NOT EXISTS `" + str(
                guild.id) + "_logs" + "` (`timestamp` TEXT, `guild_id` BIGINT, `channel_id` BIGINT, `message_id` BIGINT, `user_id` BIGINT, `action_type` TINYTEXT, `message` MEDIUMTEXT)")
    elif storage_type == "flatfile":
        print("[!] You are currently using flatfile storage type. MySQL Database is recommended")
        print_info(bot)
    print("Successfully connected to Discord.")


@bot.event
async def on_member_join(member):
    print(f'{member} joined ' + member.server.name + ".")
    print_info(f'{member} joined the server.' + member.server.name + ".")


@bot.event
async def on_member_remove(member):
    print(f'{member} left ' + member.server.name + ".")
    print_info(f'{member} left ' + member.server.name + ".")


@bot.event
async def on_message(message):
    print_debug(message)
    # if not message.author.bot:
    #     await message.channel.send(message.content)
    guild = message.guild
    if storage_type == "mysql":
        try:
            db.execute("SELECT * FROM `users` WHERE user_id = '" + str(message.author.id) + "'")
            if db.rowcount == 0:
                db.execute("INSERT INTO `users`(user_id, user_name, user_discriminator) VALUES(%s, %s, %s)",
                           (message.author.id, message.author.name, message.author.discriminator.zfill(4)))
                database.commit()
            db.execute("SELECT * FROM `channels` WHERE channel_id = '" + str(message.channel.id) + "'")
            if db.rowcount == 0:
                db.execute("INSERT INTO `channels`(channel_id, channel_name) VALUES(%s, %s)",
                           (message.channel.id, message.channel.name))
                database.commit()
            db.execute("INSERT INTO `" + str(
                guild.id) + "_logs" + "`(timestamp, guild_id, channel_id, message_id, user_id, action_type, message) VALUES(%s, %s, %s, %s, %s, %s, %s)",
                       (redtea.time(), message.guild.id, message.channel.id, message.id, message.author.id,
                        "MESSAGE_SEND", message.content))
            database.commit()
        except Exception as e:
            print(e)
            print_debug(e)
    elif storage_type == "flatfile":
        try:
            path = "logs/{}.txt".format(guild.id)
            with open(path, 'a+') as f:
                print("{0.author.name} : {0.content}".format(message), file=f)
        except Exception as ignore:
            print_debug(ignore)
    await bot.process_commands(message)


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)} ms')  # ping


@bot.command(aliases=['purge', 'remove', 'cls'])
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
        await ctx.send(f'{member} has been banned!')
        print(f'{member} has been banned!')
    except Exception as failban:
        await ctx.send("Failed to ban:" + str(failban))


@bot.command(aliases=['version', 'about', 'info', 'data'])
async def ver(ctx):
    await ctx.send(" By RedTea, ColaIan | GitHub: https://github.com/lRedTeal/TeaPot ")
    await ctx.send(" Code w/ Python <3 with Discord.py API | logged in as: " + bot.user.name)
    await ctx.send(" Build-03_pre-release | RedTeaPackage: " + redtea.version() + " | https://forum.redtea.red")


@bot.command()
async def admin(ctx):
    # Not Done Yet.
    await ctx.send("You don't have permission to perform this command!")


@bot.command()
async def join(ctx):
    try:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("TeaPot has joined " + channel)
    except:
        await ctx.send("TeaPot Already connected to a voice channel!")


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.command(pass_context=True, aliases=['p'])
# You might have to set FFMPEG to system path!
async def play(ctx, url: str):
    global nname

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print_info("No more queued song(s)")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print_info("Song done, playing next queue")
                print_info(f"song still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')
                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} has finished playing"))
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.20

            else:
                queues.clear()
                return
        else:
            queues.clear()
            print_info("No songs were queued..")

    song = os.path.isfile("song.mp3")
    try:
        if song:
            os.remove("song.mp3")
            queues.clear()
            print_info("Removed old song file")
    except PermissionError:
        print_error("Trying to delete song file, but it's being played!")
        await ctx.send("Error: Music playing, use /teapot queue [Link]")
        return

    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print_info("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
        print_info("No old Queue Folder")
    print_info("Getting everything ready now")

    voice = get(bot.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print_info("Downloading audio now...")
            await ctx.send("Downloading... Please Wait...")
            ydl.download([url])
    except Exception as faildownload:
        await ctx.send("Fail to download: " + str(faildownload))

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print_info("Renamed Audio file")
            os.rename(file, "song.mp3")
    try:
        channel = ctx.author.voice.channel
        await channel.connect
    except Exception:
        pass
    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.20

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname}")
    print_info(f"playing: {nname}")


@bot.command(pass_context=True)
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    queues.clear()
    if voice and voice.is_playing():
        print_info("Stop music")
        voice.stop()
        await ctx.send("Music Stopped")
    else:
        voice.stop()
        await ctx.send("Music not Playing, Failed to stop...")


@bot.command()
async def np(ctx):
    global nname
    await ctx.send(f"Current Playing: {nname}")


@bot.command(pass_context=True)
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num
    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.@(ext)s")
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print_info("Downloading audio now...")
            await ctx.send("Adding song" + str(q_num) + " to the queue")
            ydl.download([url])
            print_info("Song added to queue")
    except Exception as faildownload:
        await ctx.send("Fail to download: " + str(faildownload))


@bot.command()
async def test(ctx):
    print(ctx)


queues = {}

try:
    bot.run(bot_token)
except Exception as loginFailed:
    print(
        "[ERROR] Failed to connect to DiscordAPI. Please check your bot token! Make sure that you have run setup.py once!")
