import os
import re
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


@bot.command(name='help')
async def help(ctx):
    help_text = """
Enter the coordinates where you'd like to play in the chat (e.g. A1). 
If you need to enter the same coordinate twice in a row, you can switch between upper and lower case. You can also enter multiple coordinates in one message.
Other available commands: 
!link: URL for current problem; 
!review: URL of last problem; 
!rank: change the rank of the next problem (e.g. !rank 10k);
!next: skip to the next problem (can only be used after 2 minutes since last move).
    """
    await ctx.send(help_text)

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
    m = re.search(r'rank (.+)', msg)
    if m:
        if tsumego.update_rank(m.group(1)):
            await ctx.send('Rank updated, it\'ll be used on next problem.')
        else:
            await ctx.send('Invalid rank. Use 5d to 20k. E.g. !rank 10k')

@bot.command(name='code')
async def code(ctx):
    await ctx.send('https://github.com/bani/twitch-tsumego')

@bot.command(name='donate')
async def donate(ctx):
    await ctx.send('If you\'d like to contribute, I support the following orgs: https://supporters.eff.org/donate/ | https://donate.mozilla.org/ | https://donate.wikimedia.org')

if __name__ == "__main__":
    tsumego = tsumego.Tsumego()
    bot.run()

