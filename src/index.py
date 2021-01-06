import os
import discord
from discord.ext import commands
import datetime
from urllib import parse, request
import re
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='>', description='Bot de Ayuda')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def sum(ctx, a: int, b: int):
    await ctx.send(a+b)

@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f'{ctx.guild.name}', description='Lorem impsum asdas', timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name='Server created at', value=f'{ctx.guild.created_at}')
    embed.add_field(name='Server owner', value=f'{ctx.guild.owner}')
    embed.add_field(name='Server region', value=f'{ctx.guild.region}')
    embed.add_field(name='Server ID', value=f'{ctx.guild.id}')
    embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/768px-Python-logo-notext.svg.png')
    await ctx.send(embed=embed)

@bot.command()
async def yt(ctx, *, search):
    q = parse.urlencode({'search_query': search})
    html_content = request.urlopen('https://www.youtube.com/results?' + q)
    s_result = re.findall(r'watch\?v=(\S{11})', html_content.read().decode())
    #print(s_result)
    await ctx.send('https://www.youtube.com/watch?v='+ s_result[0])

# Eventos

"""
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'feliz cumpleaños' in message.content.lower():
        await message.channel.send('Feliz cumpleaños! 🎈🎉')
"""

@bot.event
async def on_ready():
    #await bot.change_presence(activity=discord.Streaming(name='Tutorial', url='http://www.twitch.tv/sokids'))
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    
    print(
        f'{bot.user} se ha conectado a Discord!\n'
        f'Se conecto a {guild.name} (id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Miembros del servidor : \n - {members}')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hola {member.name}!, bienvenido a mi servidor!'
    )

bot.run(DISCORD_TOKEN)
