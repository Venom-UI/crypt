from Crypto.PublicKey import RSA
from Crypto import Random
import ast
import discord
from discord.ext import commands
import json
import os
bot = commands.Bot(command_prefix='$', description="this is a bot", case_insensitive=True)
bot.remove_command('help')

with open("binary.json", "r") as binary_json:
    data = json.load(binary_json)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command not found. Please type "$help" for a list of commands')
        return

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Commands",description="",color=0x00ff00)
    embed.set_footer(text="For aditional help contact Venom#1519")
    embed.add_field(name="encryptb", value="`Turn words into binary.`", inline=True)
    embed.add_field(name="decryptb", value="`Turn binary into words.`", inline=True)
    embed.add_field(name="generatersa", value="`generate public and private rsa keys.`", inline=True)
    embed.add_field(name="encryptrsa", value="`encrypt the message in rsa (send only the public key).`", inline=True)
    embed.add_field(name="decryptrsa", value="`decrypt the message using rsa (WIP).`", inline=True)
    await ctx.send(embed=embed)

# Binary encrpyt
@bot.command(brief="turn message into binary")
async def encryptb(ctx, *, msg):
    msg = str(msg)
    msg1 = ""
    for word in msg:
       bin = data[word] # Look what each word in msg is in binary
       msg1 = msg1+bin+" " # Add said binary to the final message
    if len(msg1) <= 2000: # Check if msg1 has more than 2000 words if not send the message normaly if it does send a txt file with the message
        embed = discord.Embed(title="Binary",description=msg1, color=0x00ff00)
        await ctx.send(embed=embed)
    else:
        with open("binary.txt", "w") as bin:
            bin.write(msg1)
        with open("binary.txt", "r") as bin:
            await ctx.send('Too long to send in a message', file=discord.File(bin))
            os.remove('binary.txt')

# Binary decrypt
@bot.command(brief="turn binary into words")
async def decryptb(ctx, *, msg):
    if " " in msg: # remove all space from msg
        msg = msg.replace(" ","")
    msg = [msg[i:i+8] for i in range(0, len(msg), 8)] # divide in bytes
    msg1 = ""
    for word in msg: 
        if word != "11000010": # characters like ¨ need two bytes to be translated but since i'm dividing it in groups of 1 byte i just ignore the first byte
            bin = data[word]
            msg1 = msg1+bin 
    if len(msg1) <= 2000: # Check if msg1 has more than 2000 words if not send the message normaly if it does send a txt file with the message
        embed = discord.Embed(title="Binary",description=msg1, color=0x00ff00)
        await ctx.send(embed=embed)
    else:
        with open("binary.txt", "w") as bin:
            bin.write(msg1)
        with open("binary.txt", "r") as bin:
            await ctx.send('Too long to send in a message', file=discord.File(bin))
            os.remove('binary.txt')

@bot.command(brief="ban")
async def ban(ctx, user1, *, reason):
    print("a")
    print(ctx.message.author)
    if "879039825624301589" in [y.id for y in ctx.message.author.roles]:
        sus = bot.get_user(user1)
        
bot.run('TOKEN')
