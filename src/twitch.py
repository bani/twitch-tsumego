# -*- coding: utf-8 -*-

import os
import re
import logging
from twitchio.ext import commands
from dotenv import load_dotenv
import tsumego

load_dotenv()

bot = commands.Bot(
    # set up the bot
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"{os.environ['BOT_NICK']} is online!")
    logging.basicConfig(filename='../chat.log', format='%(asctime)s %(message)s', datefmt='%I:%M', level=logging.INFO)

@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'

    if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
        return

    await bot.handle_commands(ctx)

    if not re.search(r'[a-z]{2,}', ctx.content): #if there are 2+ characters it's a regular message
        m = re.findall(r'[ ,]*[a-tA-T]{1}[0-9]{1,2}', ctx.content)
        for coords in m:
            #Remove potentially leading commas and spaces
            coords = coords.strip(", ")
            #Submit move, first character is coordinate letter, second (and possibly third) character is number part
            result = tsumego.place_stone(coords[0:1], coords[1:3], ctx.author.name)
            await ctx.channel.send(result)
            if 'Keep going' not in result:
                break
    else:
        logging.info(f"{ctx.author.name}: {ctx.content}")


@bot.command(name='help')
async def help(ctx):
    help_text1 = """
Enter the coordinates where you'd like to play in the chat (e.g. A1). 
Win one point for final correct move, lose one point for incorrect ones. 
If you need to enter the same coordinate twice in a row, add some question marks to pass Twitch's spam filter (e.g. A1???). You can also enter multiple coordinates in one message.
    """
    help_text2 = """
Other available commands: 
!rank: change the rank of the next problem (e.g. !rank 10k); 
!next: skip to the next problem (can only be used after 2 minutes since last move); 
!review: URL of previous problem; 
!link: URL for current problem; 
!points: check your current points
    """
    await ctx.send(help_text1)
    await ctx.send(help_text2)

@bot.command(name='points')
async def points(ctx):
    user = ctx.message.author.name
    points = tsumego.players[user] if user in tsumego.players else 0
    if user == 'beginnergo': points = '-∞'
    await ctx.send(f"{user} has {points} points")

@bot.command(name='review')
async def review(ctx):
    await ctx.send(tsumego.url)

@bot.command(name='link')
async def link(ctx):
    await ctx.send(tsumego.driver.current_url)

@bot.command(name='next')
async def next(ctx):
    wait = tsumego.next()
    if wait > 0:
        await ctx.send(f'Please wait {int(wait)} seconds before trying to go to the next problem.')

@bot.command(name='rank')
async def rank(ctx):
    msg = ctx.message.clean_content
    m = re.search(r'rank ([0-9]{1,2}[kd])', msg)
    if m:
        r = m.group(1)
        v = f"{r[:-1]} {'kyu' if r[-1] == 'k' else 'dan'}"

        if tsumego.update_rank(v):
            await ctx.send('Rank updated, it\'ll be used on next problem.')
        else:
            await ctx.send('Invalid rank. Use 5d to 20k. E.g. !rank 10k')
    else:
        await ctx.send('Use format !rank 10k')

@bot.command(name='coords')
async def coords(ctx):
    tsumego.coordinates()

@bot.command(name='output')
async def output(ctx):
    print(tsumego.players)

@bot.command(name='leaderboard')
async def leaderboard(ctx):
    i = 1
    for (k,v) in sorted(tsumego.players.items(), key=lambda x: -x[1]):
        print(f"{str(i).rjust(2)}. {k.ljust(20)} {str(v).rjust(3)}")
        i+=1

@bot.command(name='code')
async def code(ctx):
    await ctx.send('https://github.com/bani/twitch-tsumego')


if __name__ == "__main__":
    tsumego = tsumego.Tsumego()
    bot.run()

