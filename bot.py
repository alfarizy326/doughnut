import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import logging
import sqlite3awdsad
import time
import random
from discord import Game
from keep_alive import keep_alive
import aiohttp
import os

logging.basicConfig(level=logging.INFO)

Client = discord.client
client = commands.Bot(command_prefix = "!d ", status=discord.Status.idle, activity=discord.Game(name="Booting.."))
Clientdiscord = discord.Client()
client.remove_command("help")

def threshold(n):
    level_threshold = 5*(n**2)+50*n+100
    return level_threshold

@client.event
async def on_message(message):

    if message.author == client.user:
        return
    if message.author.bot:
        return

    if message.content.startswith('l>'):
        await client.process_commands(message)
        return
        
    db = sqlite3.connect('data/users.db')
    c = db.cursor()

    c.execute('SELECT * FROM users WHERE id= ?', (message.author.id,))
    user = c.fetchone()
        
    if user is None:
        await bot.send_message(message.channel, 'Looks like you\'re new! Welcome to level 1. Initializing player...')
        c.execute('INSERT INTO users(id, name, level, exp, rawexp, time) VALUES(?,?,?,?,?,?)', (message.author.id, message.author.name, 1, 0, 0, time.time()))
        db.commit()
        db.close()
        return

    if message.author.name != user[1]:
        c.execute('UPDATE users SET name = ? WHERE id= ?', sssawdsa(message.author.name, message.author.id))

    if (time.time() - user[5]) > 60:
        addedexp = random.randint(10, 25)
        exp = user[3] + addedexp
        rawexp = user[4] + addedexp
        c.execute('UPDATE users SET exp = ?, rawexp = ?, name = ?, time = ? WHERE id= ?', (exp, rawexp, message.author.name, time.time(), message.author.id))

        if (exp > threshold(user[2])):
            level = user[2] + 1
            c.execute('UPDATE users SET exp = ?, level = ? WHERE id= ?', (0, level, message.author.id))
            await bot.send_message(message.channel, 'Wowza! You leveled up! Your level is now **{}**.'.format(level))

    db.commit()
    db.close()

    await bot.process_commands(message)

@client.event
async def on_ready():
    print("BOT SERVER is ready!")
    print("Ready to go!")
    print(f"Server: {len(client.guilds)} guilds.")
    print("Username and Unknown is the best!")
    print(discord.__version__)
    print(discord.version_info)
    activity = discord.Activity(name='bot help', type=discord.ActivityType.listening)
    await client.change_presence(activity=activity)

@client.command(pass_context=True)
async def help(ctx):
  embed = discord.Embed(title='List of Commands',
  color=0x8a4b32,
  timestamp=ctx.message.created_at)

  embed.set_footer(text=f"Requested by {ctx.author}",
    icon_url=ctx.author.avatar_url)

  embed.add_field(name='!dsb <message>', value='Sends messages to all users in the server', inline=False)
  embed.add_field(name='!dban <member> [reason]', value='Bans a member from the server', inline=False)
  embed.add_field(name='!dkick <member> [reason]', value='Kicks a member from the server', inline=False)
  embed.add_field(name='!dmute <member>', value='Mutes a member', inline=False)
  embed.add_field(name='!dunmute <member>', value='Unmutes a member', inline=False)
  embed.add_field(name='!duserinfo <member>', value='Shows information about the user', inline=False)
  embed.add_field(name='!davatar <member>', value='Shows the user avatar', inline=False)
  embed.add_field(name='!dclear <number of message>', value='Clear messages in particular channel', inline=False)
  embed.add_field(name='!dabout', value='Shows information about the bot', inline=False)
  embed.add_field(name='!dping', value='Shows your Internet speed', inline=False)
  embed.add_field(name='!daddrole <role> <member>', value='Adds a mentioned role to the mentioned user', inline=False)
  embed.add_field(name='!dremoverole <role> <member>', value='Removes a mentioned role from the mentioned user', inline=False)
  embed.add_field(name='!dnick <member>', value='Change the user nickname', inline=False)
  embed.add_field(name='!dwarn <member> [reason]', value='Warns a member', inline=False)
  await ctx.send(embed=embed)


@client.command(pass_context=True)
async def rank(ctx):
    
    try:
        _, member = (ctx.message.content).split(' ', 1)
        member = re.sub("[^0-9]", "", member)
    except:
        member = ctx.message.author.id
    
    db = sqlite3.connect('data/users.db')
    c = db.cursor()

    c.execute('SELECT user.*, (SELECT count(*) FROM users AS members WHERE members.rawexp > user.rawexp) as Rank FROM users AS user WHERE id = ?',
              (ctx.message.author.id, ))
    
    user = c.fetchone()
    db.close()

    rank = str(user[6] + 1)

    embed = discord.Embed(title='{}\'s Information'.format(ctx.message.author.name)) \
            .set_thumbnail(url=ctx.message.author.avatar_url) \
            .add_field(name='Rank', value='#' + rank) \
            .add_field(name='Level', value=user[2]) \
            .add_field(name='EXP', value='{}/{}'.format(user[3], threshold(user[2]))) \
            .add_field(name='Raw EXP', value=user[4]) \

    await bot.say(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member:discord.User = None, reason = None):
    if member == ctx.message.author:
        await ctx.channel.send("Why would you do that? :thinking:")
    if not member:
        await ctx.send("Please specify a **member**.")      
        return
    if reason == None:
        reason = "no reason at all!"
    message = f"You have been banned from {ctx.guild.name} for {reason}!"
    await member.send(message)
    await ctx.guild.ban(member)
    await ctx.channel.send(f"{member} has been **banned**!")
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You cant to do that")

@client.command(pass_context=True, no_pm=True)
@commands.has_permissions(administrator=True)
async def avatar(ctx, member: discord.Member):
    embed = discord.Embed(title= 'Profile picture has been stealed.',color=0x8a4b32,timestamp=ctx.message.created_at)

    embed.set_footer(text=f"Stealed by {ctx.author}", 
    icon_url=ctx.author.avatar_url)

    await ctx.send("{}".format
    (member.avatar_url))
    await ctx.send(embed=embed)
@avatar.error
async def avatar_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You cant to do that")

@client.command()
@commands.has_permissions(administrator=True)
async def info(ctx, member: discord.Member):

    roles = [role for role in member.roles]

    embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

    embed.set_author(name=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url,)

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Guild Name:", value=member.display_name)

    embed.add_field(name="Created at:",value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %P UTC"))
    embed.add_field(name="Joined at:",value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %P UTC"))

    embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
    embed.add_field(name="Top role", value=member.top_role.mention, inline=False)

    embed.add_field(name="Bot?", value=member.bot)

    await ctx.send(embed=embed)
@info.error
async def info_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You cant use that")

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def about(ctx):
  embed = discord.Embed(
        title = '',
        description = '',
        color=0x8a4b32, timestamp=ctx.message.created_at)
  embed.add_field(name='BOT SERVER', value='Created by Naufal#6366 ft. Unknown', inline=False)
  embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url,)
  await ctx.send(embed=embed)
@about.error
async def about_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You cant to do that") 
         
@client.command()
@commands.has_permissions(administrator=True)
async def ping(ctx):
    ping = client.latency
    ping = round(ping * 1000)
    embed = discord.Embed(
        title = '',
        description = '',
        color=0x8a4b32)
    embed.add_field(name='Pong!', value=f'Your ping is {ping}ms.', inline=False)
    await ctx.send(embed=embed)
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You cant to do that")

@client.command()
@commands.has_permissions(administrator=True)
async def say(ctx, *, something):
  await ctx.message.delete()
  if something is None:
    await ctx.send("What You Gonna Say?")
  else:
      await ctx.send(f"{something}")
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You cant to do that")

@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member:discord.Member = None, reason = None):
    if member == ctx.message.author:
        await ctx.channel.send("Why would you do that? :thinking:")
    if not member:
        await ctx.send("Please specify a **member**.")    
        return
    if reason == None:
        reason = "No reason at all!"
    message = f"You have been kicked from {ctx.guild.name} for {reason}!"
    await member.send(message)
    await ctx.guild.ban(member)
    await ctx.channel.send(f"{member} has been **kicked**!")
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You cant to do that")

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member=None):
    if not member:
        await ctx.send("Please specify a **member**.")
        return
    await ctx.send(f"{member.mention} got **muted**!")    
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    role = discord.utils.get(ctx.guild.roles, name="God's Fans")
    await member.remove_roles(role)
    
@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You cant to fo that")
 
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member=None):
    if not member:
        await ctx.send("Please specify a **member**")
        return
    await ctx.send(f"{member.mention} got **unmuted**!")    
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
    role = discord.utils.get(ctx.guild.roles, name="God's Fans")
    await member.add_roles(role) 
@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You cant to do that")

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def statusp(ctx, status, statuss):
  await ctx.message.delete()
  activity = discord.Activity(name=f'{status} {statuss}', type=discord.ActivityType.playing)
  await client.change_presence(activity=activity)
  await ctx.send(f"***Bot status changed to {status} {statuss}***")
@statusp.error
async def statusp_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You cant to do that")

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def statusl(ctx, status, statuss):
  await ctx.message.delete()
  activity = discord.Activity(name=f'{status} {statuss}', type=discord.ActivityType.listening)
  await client.change_presence(activity=activity)
  await ctx.send(f"***Bot status changed to {status} {statuss}***")
@statusl.error
async def statusl_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You cant use that")

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def statusw(ctx, status, statuss, statusss):
  await ctx.message.delete()
  activity = discord.Activity(name=f'{status} {statuss} {statusss}', type=discord.ActivityType.watching)
  await client.change_presence(activity=activity)
  await ctx.send(f"***Bot status changed to {status} {statuss} {statusss}***")
@statusw.error
async def statusw_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You cant to do that")

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def resetstatus(ctx):
  await ctx.message.delete()
  activity = discord.Activity(name='!dhelp', type=discord.ActivityType.Game)
  await client.change_presence(activity=activity)
  await ctx.send("***Bot status resetted.***")
@resetstatus.error
async def resetstatus_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You cant to do that")

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def sb(ctx, *, message):
    await ctx.message.delete()
    for member in ctx.guild.members:
        try:
            await member.send(message)
            print(f"{user.name} has received the message.")
        except:
            print(f"{user.name} has NOT received the message.")
    print("Action Completed: sb")
@sb.error
async def sb_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You are not allowed to sb!") 

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
@clear.error
async def clear_error(ctx, error):
  if isinstance(error, command.CheckFailure):
    await ctx.send("You are not allowed to clear messages")

@client.command(pass_context=True)
@commands.has_permissions(administrator=True) # This must be exactly the name of the appropriate role
async def r(ctx, role: discord.Role, member: discord.Member=None):
  await ctx.send("**Role added.**")
  await member.add_roles(role, member)
@r.error
async def r_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You are not allowed to add role!")

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def rr(ctx, role: discord.Role, member: discord.Member=None):
  await ctx.send("**Role removed.**")
  await member.remove_roles(role, member)
@rr.error
async def rr_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You are not allowed to remove role!")
        
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def nick(ctx, rename_too, member: discord.Member = None):
  if not member:
    await ctx.send("Please specify a **member**")
    return
  await member.edit(nick=rename_too)
  await ctx.send("**Nickname changed!**")
@nick.error
async def nick_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("**You are not allowed to change other user nickname!**")             

@client.command()
@commands.has_permissions(administrator=True)
async def invite(ctx):
    embed = discord.Embed(
        title = 'Invite me!',
        description = '',
        color=0x00ff00)
    embed.add_field(name='Link:', value='https://discordapp.com/api/oauth2/authorize?client_id=566241542075973644&permissions=0&scope=bot', inline=False)
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member:discord.User = None, reasons = None, reasonss = None, reasonsss = None, reasonssss = None, reasonsssss = None, reasonssssss = None, reasonsssssss = None, reasonssssssss = None, reasonsssssssss = None, reasonssssssssss = None,):
    if member == ctx.message.author:
        await ctx.channel.send("Why would you do that? :thinking:")
    if not member:
        await ctx.send("Please specify a **member**.")      
        return
    if reasons == None:
      reasons = "no reason at all."
    if reasonss == None:
      reasonss = ""
    if reasonsss == None:
      reasonsss = ""
    if reasonssss == None:
      reasonssss = ""
    if reasonsssss == None:
      reasonsssss = ""
    if reasonssssss == None:
      reasonssssss = ""
    if reasonsssssss == None:
      reasonsssssss = ""
    if reasonssssssss == None:
      reasonssssssss = ""
    if reasonsssssssss ==  None:
      reasonsssssssss = ""
    if reasonssssssssss ==  None:
      reasonssssssssss = ""                                 
    message = f"You were warned in {ctx.guild.name} for: {reasons} {reasonss} {reasonsss} {reasonssss} {reasonsssss} {reasonssssss} {reasonsssssss} {reasonssssssss} {reasonsssssssss} {reasonssssssssss}"
    await member.send(message)
    await ctx.channel.send(f"{member.mention} ```has been warned for {reasons} {reasonss} {reasonsss} {reasonssss} {reasonsssss} {reasonssssss} {reasonsssssss} {reasonssssssss} {reasonsssssssss} {reasonssssssssss}```")
@warn.error
async def warn_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You cant use that")

keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run('NTc1Mjk1MDk2NjEwNjE5Mzkz.XNLIbw.MXlBNz1j3hUrPN6kMbXUeOZ389E')
