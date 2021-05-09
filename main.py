from keep_alive import keep_alive
import os
import discord
import asyncio
import random
import functions
import requests

from discord.ext import commands
from pretty_help import DefaultMenu, PrettyHelp

bot = commands.Bot(command_prefix="$")

nav = DefaultMenu("◀️", "▶️")
bot.help_command = PrettyHelp(navigation=nav, color=discord.Colour.green())

# print(len(bot.guilds), bot.guilds)
  
@bot.event
async def on_ready():
  print("I'm in")
  print("number of server I'm in:", len(bot.guilds))

class Quiz(commands.Cog):
  """ Use "$quiz <time for each question>" to start the quiz. The deafault time is 30 seconds for each question. Use the "skip" command to skip the question. Use the "quit" command to quit the quiz. DM Light_Yagami#6883 or RishiNandha Vanchi#3379 if you need any help or you have any quesries regarding the bot"""
  @commands.command(
    name="quiz",
    brief="Answer some questions",
    help='Use "$quiz" command to start the quiz'
  )
  
  async def _work(self, message, timeout_=60, ques="default"):

    channel=message.channel
    if ques != "default":
      ques = str(message.author.id) + "_" + ques

    questions=functions.questions(ques)
    order=list(range(1,len(questions)))
    #order=[55,56]
    random.shuffle(order)
    # print(order)
    correct, wrong, skipped, continoustimeout = dict(), 0, 0, 0

    for i in order:
      embed=discord.Embed(title=questions[i][0], color=discord.Color.blue(),url="",description=questions[i][3])
      await channel.send(embed=embed)
          
      def funcc(x):

        return ((functions.format(x.content,questions[i][4]) == functions.format(questions[i][1],questions[i][4])) or (x.content == "quit") or (x.content == "skip") or (x.content=="stop")) and x.channel==channel

      try:
        global msg
        msg = await bot.wait_for('message', check=funcc,timeout=float(timeout_))


      except asyncio.TimeoutError:
        wrong += 1
        await channel.send("Timeout!, The Answer was:")
        embed2 = discord.Embed(title="", color=discord.Color.red(),url="",description=questions[i][1])
        await channel.send(embed=embed2)
        if len(questions[i][2])>0:
          await channel.send(questions[i][2])
        order.append(i)
        pass

      else:
        if msg.content == "quit" or msg.content=="stop":
          await channel.send('{.author} has stopped the quiz'.format(msg))
                    
          correct=sorted(correct.items(), key=lambda x: x[1], reverse=True)
          embed5=discord.Embed(color=0xb1dd8b,title="Scores:")
          for j in correct:
            embed5.add_field(name=str(j[0])[:-5]+":",value=str(j[1]),inline=False)
          embed5.add_field(name="Skipped:",value=str(skipped),inline=False)
          embed5.add_field(name="Wrong:",value=str(wrong),inline=False)
          await channel.send(embed=embed5)
          break


        if msg.content == "skip":
          skipped += 1
          await channel.send("Skipped!, The Answer was:")
          embed2 = discord.Embed(title="", color=discord.Color.red(),url="",description=questions[i][1])
          await channel.send(embed=embed2)
          if len(questions[i][2])>0:
            await channel.send(questions[i][2])
          order.append(i)
          continue
        
        else: 
          if msg.author in correct:
            correct[msg.author] += 1
          else:
            correct[msg.author]=1
          s = '{.author} got the correct answer! \n' + questions[i][2]
          await msg.channel.send(s.format(msg))
          if i==order[-1]:
                        
            correct=sorted(correct.items(), key=lambda x: x[1], reverse=True)
            embed5=discord.Embed(color=0xb1dd8b,title="Scores:")
            for j in correct:
              embed5.add_field(name=str(j[0])[:-5]+":",value=str(j[1]),inline=False)
            embed5.add_field(name="Skipped:",value=str(skipped),inline=False)
            embed5.add_field(name="Wrong:",value=str(wrong),inline=False)
            await channel.send(embed=embed5)
            embed4=discord.Embed(title="Conquered!",color=discord.Color.gold(),url="https://www.youtube.com/watch?v=Utgrbq_CFt4",description="GGs!, You are dang OP")
            await channel.send(embed=embed4)

class NewDeck(commands.Cog):
  '''Add your own reactions using this command'''
  @commands.command(
    name="nd"
  )

  async def _work(self, ctx):
    await ctx.channel.send("Send the reactions which you want to add in appropriate format:")

    def funccc(x):
      if x.author.id == ctx.author.id:
        return True
    
    msg2 = await bot.wait_for('message', check=funccc)
    await msg2.channel.send("Name of the new deck:")
    msg3 = await bot.wait_for('message', check=funccc)
    file_name = str(msg2.author.id) + "_" + msg3.content + ".csv"
    file_url = msg2.attachments[0]
    r = requests.get(file_url)

    if str(file_url)[-3:]=="csv":
      open(file_name,"wb").write(r.content)
      
    else:
      with open(file_name,"w") as f:      
        f.write(r.text)
        f.close()

    await msg2.channel.send(str(msg3.content)+" was added to "+str(msg2.author)+"\'s database!")


class invite(commands.Cog):
  @commands.command(name="invite")
  

  async def _work(self, ctx):
    invite_link="https://discord.com/api/oauth2/authorize?client_id=836658126684946432&permissions=2148006977&scope=bot"
    await ctx.channel.send(invite_link)
class download(commands.Cog):
  @commands.command(name="download")
  
  async def _word(self, ctx, ques):
    ques1=str(ctx.author.id)+'_'+ques+".csv"
    await ctx.send(file=discord.File(ques1,filename=ques+".csv"))

bot.add_cog(NewDeck(bot))
bot.add_cog(invite(bot))
bot.add_cog(download(bot))

bot.add_cog(Quiz(bot))
keep_alive()
bot.run(os.getenv("TOKEN"))