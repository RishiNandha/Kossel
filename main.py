from keep_alive import keep_alive
import discord
import os
import asyncio
import requests
import json
import random
from replit import db
import functions

from discord.ext import commands
from pretty_help import DefaultMenu, PrettyHelp

bot = commands.Bot(command_prefix="$")

nav = DefaultMenu("◀️", "▶️", "❌")
bot.help_command = PrettyHelp(navigation=nav, color=discord.Colour.green())

  
@bot.event
async def on_ready():
  print("I'm in")

class Quiz(commands.Cog):
  """ All Quiz commands """
  @commands.command(
    name="quiz",
    brief="Answer some questions",
    help="Use this command to work and earn a random amount of money"
  )
  
  async def _work(self, ctx):

    questions=functions.questions("reactions")
    order=list(range(1,len(questions)))
    random.shuffle(order)

    for i in order:
      await ctx.send(questions[i][0])
          
      #msg_ch = None
      def funcc(x):
        #global msg_ch
        #msg_ch = msg.channel
        return functions.format(x.content) == questions[i][1]
        
      #msg = await bot.wait_for('message', check=funcc)
      
      try:
        global msg
        msg = await bot.wait_for('message', check=funcc,timeout=5.0)


      except asyncio.TimeoutError:
        
        # # a = 'The correct answer was'+ functions.pack_answer_set(questions[i][1])
        # # # await msg.channel.send(a)
        # await msg.channel.send("timeout, {ans}".format(ans=a))
        #global msg_ch
        #await msg_ch.send("timeout")
        await ctx.send("timeout")
        order.append(i)
        pass

      else:
        await msg.channel.send('{.author} got the correct answer!'.format(msg))
      # msg = await bot.wait_for('message', check=funcc)
      # await msg.channel.send('{.author} got the correct answer!'.format(msg))

# @client.event
# async def on_message(message):
#   if message.author == client.user:
#     return

#   msg = message.content

#   if msg.startswith("$inspire"):
#     quote = get_quote()
#     await message.channel.send(quote)

#   if db["responding"]:
#     options = starter_encouragements
#     # if "encouragements" in db.keys():
#     #   print(type(db["encouragements"]))
#     #   options = options + db["encouragements"]

#   if any(word in msg for word in sad_words):
#      await message.channel.send(random.choice(options))

#   if msg.startswith("$new"):
#     encouraging_message = msg.split("$new ",1)[1]
#     update_encouragements(encouraging_message)
#     await message.channel.send("New encouraging message added.")

#   if msg.startswith("$del"):
#     encouragements = []
#     if "encouragements" in db.keys():
#       index = int(msg.split("$del",1)[1])
#       delete_encouragment(index)
#       encouragements = db["encouragements"]
#     await message.channel.send(encouragements)

#   if msg.startswith("$list"):
#     encouragements = []
#     if "encouragements" in db.keys():
#       encouragements = db["encouragements"]
#     await message.channel.send(encouragements)
    
#   if msg.startswith("$responding"):
#     value = msg.split("$responding ",1)[1]

#     if value.lower() == "true":
#       db["responding"] = True
#       await message.channel.send("Responding is on.")
#     else:
#       db["responding"] = False
#       await message.channel.send("Responding is off.")

bot.add_cog(Quiz(bot))
keep_alive()
bot.run(os.getenv("TOKEN"))