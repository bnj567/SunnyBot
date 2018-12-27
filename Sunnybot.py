# -*- coding: utf-8 -*-
# Sunny Bot

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import json
import os
import time
import math
import requests

botprefix="sun-"
bot = commands.Bot(command_prefix=botprefix)
os.chdir(r"D:\Sunnybot")

subscription_key = "8f057ed2229d4855a87ab0f405928778"
assert subscription_key
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

@bot.event
async def on_ready():
	print ("Ready when you are XD")
	print ("I am running on " + bot.user.name)
	print ("With the id " + bot.user.id)
	
@bot.event
async def on_message(message):
        with open(r"D:\Sunnybot\users.json", mode="r") as f:
                users = json.load(f)

        await update_data(users, message.author, message.server)

        with open(r"D:\Sunnybot\users.json", mode="w") as f:
                users = json.dump(users, f)
                
        if message.content.startswith(botprefix + '8ball'):
                await bot.send_message(message.channel, random.choice(["Definitely ", "Its highly likely ", "Maybe ", "Its not likely ", "Certainly not ", "Of course not, smh my head ", "How would i know? "]) + str(message.author.name))
        elif message.content.lower() == 'ayy' or message.content.lower() == 'ayyy':
                await bot.send_message(message.channel, "I'd say lmao but that would be annoying")
        elif message.content.lower() == 'vriska':
                await bot.send_message(message.channel, "vriska did nothing wrong.")
                print(message.author)
        elif message.content.lower() == 'secretcreditscommand':
                await bot.send_message(message.channel, "Credit to: bnj567#8316 (Programmer), Sunny ☿ Waifu#0955 (Sunny), The Sunny Side Up community, and that other shit that developers say about you the user for using the bot.")
        elif 'nigger' in message.content.lower() or 'nigga' in message.content.lower():
                with open(r"D:\Sunnybot\users.json", mode="r") as f:
                        users = json.load(f)

                await update_data(users, message.author, message.server)
                        
                if users[message.author.id + message.server.id]['hasnwordpass'] == 0:
                        await bot.send_message(message.channel, "Im afraid i'm going to have to kill you now.")
                else:
                        print(message.author.name + " has the n-word pass so i'll let it slide.")
                
                with open(r"D:\Sunnybot\users.json", mode="w") as f:
                        users = json.dump(users, f)
                
        elif message.content.startswith(botprefix + 'daily'):
                with open(r"D:\Sunnybot\users.json", mode="r") as f:
                        users = json.load(f)

                await update_data(users, message.author, message.server)
                await daily(users, message.author, message.server, message.channel)

                with open(r"D:\Sunnybot\users.json", mode="w") as f:
                        users = json.dump(users, f)
        elif message.content.startswith(botprefix + 'balance') or message.content.startswith(botprefix + 'bal'):
                with open(r"D:\Sunnybot\users.json", mode="r") as f:
                        users = json.load(f)

                await update_data(users, message.author, message.server)
                await bot.send_message(message.channel, "You currently have: :sunny: :dollar: {} sunbux".format(users[message.author.id + message.server.id]['sunbux']))

                with open(r"D:\Sunnybot\users.json", mode="w") as f:
                        users = json.dump(users, f)
        elif message.content.startswith(botprefix+"search"):
                await searchimg(message.content.replace(botprefix+"search", ""), message.channel)
        elif message.content.startswith(botprefix+"help") or message.content.startswith(botprefix+"commands"):
                embed=discord.Embed(title="Sunnybot Commands", description="'sun-' is the default command prefix", color=0xffff00)
                embed.add_field(name="8ball", value="predict the future and answer deep questions", inline=False)
                embed.add_field(name="ayy/ayyy", value="this isn't qtChan i swear", inline=False)
                embed.add_field(name="daily", value="get your daily 200 sunbux", inline=False)
                embed.add_field(name="bal/balance", value="check how much sunbux you have", inline=False)
                embed.add_field(name="search", value="find an image on the internet", inline=False)
                embed.set_footer(text="More coming soon, + A whole bunch of eastereggs")
                await bot.send_message(message.channel,embed=embed)
        elif message.content == botprefix+"shop" or message.content == botprefix+"buy":
                embed=discord.Embed(title="Sunnybot Shop", description="Capitalism at its finest", color=0xffff00)
                embed.add_field(name="sun-buy nwordpass", value="Allows you to say the n-word 5000SUNBUX", inline=True)
                embed.set_footer(text="More coming soon")
                await bot.send_message(message.channel,embed=embed)
        elif message.content == botprefix+"buy nwordpass":
                with open(r"D:\Sunnybot\users.json", mode="r") as f:
                        users = json.load(f)

                await update_data(users, message.author, message.server)
                if users[message.author.id + message.server.id]['sunbux'] >= 5000 and users[message.author.id + message.server.id]['hasnwordpass'] == 0:
                        users[message.author.id + message.server.id]['sunbux'] = users[message.author.id + message.server.id]['sunbux'] - 5000
                        users[message.author.id + message.server.id]['hasnwordpass'] = 1
                        await bot.send_message(message.channel,"You now have the nword pass")
                else:
                        await bot.send_message(message.channel,"Something went wrong, Either you cannot afford the item or you have the pass.")
                        

                with open(r"D:\Sunnybot\users.json", mode="w") as f:
                        users = json.dump(users, f)
@bot.event
async def on_member_join(member):
        with open(r"D:\Sunnybot\users.json", mode="r") as f:
                users = json.load(f)

        await update_data(users, member, member.server)

        with open(r"D:\Sunnybot\users.json", mode="w") as f:
                users = json.dump(users, f)

async def update_data(users, user, guild):
        if not user.id + guild.id in users:
                users[user.id + guild.id] = {}
                users[user.id + guild.id]['sunbux'] = 0
                users[user.id + guild.id]['name'] = user.name
                users[user.id + guild.id]['server'] = guild.name
                users[user.id + guild.id]['thisdaily'] = 0
                users[user.id + guild.id]['hasnwordpass'] = 0
                users[user.id + guild.id]['inventory'] = []

async def add_cash(users, user, money, guild):
        users[user.id + guild.id]['sunbux'] += money

async def daily(users, user, guild, channel):
        if users[user.id + guild.id]['thisdaily'] <= time.time():
                users[user.id + guild.id]['thisdaily'] = time.time() + 86400
                await add_cash(users, user, 200, guild)
                await bot.send_message(channel, "You have claimed you daily and gained 200 :sunny: :dollar: sunbux")
                await bot.send_message(channel, "Your new balance is {} :sunny: :dollar: sunbux".format(users[user.id + guild.id]['sunbux']))
        else:
                await bot.send_message(channel, "You already claimed your daily :rolling_eyes: try again at {}".format(time.ctime(users[user.id + guild.id]['thisdaily'])))

async def searchimg(searchterm, channel):
        headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
        params  = {"q": searchterm, "license": "public", "imageType": "photo"}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        await bot.send_message(channel, "Search results: \n" + random.choice([img["thumbnailUrl"] for img in search_results["value"][:16]]) + "\n\n" + random.choice([img["thumbnailUrl"] for img in search_results["value"][:16]]))
        

#@bot.command(pass_context=True)
#async def eightball(ctx, user: discord.Member):
#	await bot.say(random.choice("Definetly ", "Its highly likely ", "Maybe ", "Its not likely ", "Certainly not ", "Of course not, smh my head ", "How would i know? ") + user.name
	
bot.run("NTI1ODg0OTkwNTE3NTQyOTE5.Dv9JDg.iLfwiY9_2jqm-nEDEWjNztV04Yg")
