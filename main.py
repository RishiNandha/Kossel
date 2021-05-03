from keep_alive import keep_alive
import discord
import os
import asyncio

import random

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
      embed=discord.Embed(title=questions[i][0], color=discord.Color.blue(),url="",description="")
      await ctx.send(embed=embed)
          
      def funcc(x):

        return functions.format(x.content) == functions.format(questions[i][1])

      try:
        global msg
        msg = await bot.wait_for('message', check=funcc,timeout=5.0)


      except asyncio.TimeoutError:

        await ctx.send("Timeout!, The Answer was **"+questions[i][1]+"**\n"+questions[i][2])
        order.append(i)
        pass

      else:
        s = '{.author} got the correct answer! \n' + questions[i][2]
        await msg.channel.send(s.format(msg))

bot.add_cog(Quiz(bot))
keep_alive()
bot.run(os.getenv("TOKEN"))