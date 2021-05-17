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
  
async def send_quit_embed(correct, skipped, timeout, channel):
  correct=sorted(correct.items(), key=lambda x: x[1], reverse=True)
  embed5=discord.Embed(color=0xb1dd8b,title="Scores:")
  for j in correct:
    embed5.add_field(name=str(j[0])[:-5]+":",value=str(j[1]),inline=False)
  embed5.add_field(name="Skipped:",value=str(skipped),inline=False)
  embed5.add_field(name="Timeout:",value=str(timeout),inline=False)
  await channel.send(embed=embed5)

async def send_quit_embed_sm2(correct, skipped, timeout, channel):
  correct=sorted(correct.items(), key=lambda x: x[1], reverse=True)
  embed6=discord.Embed(color=0xb1dd8b,title="Progress:")
  for j in correct:
    embed6.add_field(name="Cards moved to higher level"+":",value=str(j[1]),inline=False)
  embed6.add_field(name="Cards moved back to level 1:",value=str(skipped+timeout),inline=False)
  await channel.send(embed=embed6)

@bot.event
async def on_ready():
  print("I'm in")
  print("number of server I'm in:", len(bot.guilds))

class Quiz(commands.Cog):
  """ Use "$quiz <time for each question>" to start the quiz. The deafault time is 30 seconds for each question. Use the "skip" command to skip the question. Use the "quit" command to quit the quiz. DM Light_Yagami#6883 or RishiNandha Vanchi#3379 if you need any help or you have any quesries regarding the bot."""
  @commands.command(
    name="quiz",
    brief="Answer some questions",
    help='Use "$quiz" command to start the quiz'
  )
  
  async def _work(self, message, timeout_=60, ques="default"):
    

    ques2 = ques
    channel=message.channel
    if ques not in [x.split('.')[0] for x in os.listdir()]:
      ques = str(message.author.id) + "_" + ques
    try:
      questions=functions.questions(ques)
    except FileNotFoundError:
      fnfe = "The reaction deck named '" + ques2 + "' was not found! Use the '$nd' command to add a new deck."
      await channel.send(fnfe)
      return None


    order=list(range(1,len(questions)))
    #order=[55,56]
    random.shuffle(order)
    # print(order)
    correct, timeout, skipped, continoustimeout = dict(), 0, 0, 0

    for i in order:
      progress='\n' + str(round(sum(correct.values())/(len(questions)-1)*100,1)) + "% quiz completed"
      embed=discord.Embed(title=questions[i][0], color=discord.Color.blue(),url="",description=(questions[i][3]+progress))
      await channel.send(embed=embed)
          
      def funcc(x):

        return ((functions.format(x.content,questions[i][4]) == functions.format(questions[i][1],questions[i][4])) or (x.content == "quit") or (x.content == "skip") or (x.content=="stop")) and x.channel==channel

      try:
        global msg
        msg = await bot.wait_for('message', check=funcc,timeout=float(timeout_))


      except asyncio.TimeoutError:
        timeout += 1
        continoustimeout += 1
        if continoustimeout > 9:
          await channel.send("Stopping the quiz because the last 10 questions went unanswered.")
          await send_quit_embed(correct, skipped, timeout, channel)
          break
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
          
          await send_quit_embed(correct, skipped, timeout, channel)
          break


        if msg.content == "skip":
          skipped += 1
          continoustimeout = 0
          skip_send = "Skipped!, The Answer was:"
          await channel.send(skip_send)
          embed2 = discord.Embed(title="", color=discord.Color.red(),url="",description=(questions[i][1]))
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
          continoustimeout = 0
          s = '{.author} got the correct answer! \n' + questions[i][2] 
          await msg.channel.send(s.format(msg))
          if i==order[-1]:
                        
            await send_quit_embed(correct, skipped, timeout, channel)
            embed4=discord.Embed(title="Conquered!",color=discord.Color.gold(),url="https://www.youtube.com/watch?v=Utgrbq_CFt4",description="GGs!, You are dang OP")
            await channel.send(embed=embed4)

class NewDeck(commands.Cog):
  '''Add your own reactions using this command'''
  @commands.command(
    name="nd",
    help="Add your own reactions using this command. Use "
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

class serverinvite(commands.Cog):
  @commands.command(name="serverinvite")
  

  async def _work(self, ctx):
    invite_link="https://discord.gg/X6zkYTan"
    await ctx.channel.send(invite_link)

class invite(commands.Cog):
  @commands.command(name="invite")
  

  async def _work(self, ctx):
    invite_link="https://tinyurl.com/ankikopybotinvite"
    await ctx.channel.send(invite_link)
class download(commands.Cog):
  @commands.command(name="download")
  
  async def _word(self, ctx, ques="default"):
    if ques in [x.split('.')[0] for x in os.listdir()]:
      ques1=ques+".csv"
    else:
      ques1=str(ctx.author.id)+'_'+ques+".csv"
    await ctx.send(file=discord.File(ques1,filename=ques+".csv"))

class update(commands.Cog):
  @commands.command(name="update")
  async def _work(self,message,ques):
    if int(message.author.id) in [829374685480615946,299120006438846465,773182724957536307,812609048511381524,562608039224410112]:
      open(str(ques)+".csv","wb").write(requests.get(message.message.attachments[0]).content)
      await message.channel.send("Updation Complete!")
bot.add_cog(update(bot))

class publicdecks(commands.Cog):
  @commands.command(name="publicdecks")
  async def _work(self,ctx):
    await ctx.channel.send("Public decks:")
    for i in os.listdir():
      if i[0] not in [str(j) for j in range(10)] and i[-3:]=="csv":
        await ctx.channel.send(" - "+i.split(".")[0])
bot.add_cog(publicdecks(bot))

class announce(commands.Cog):
  @commands.command(name="announce")
  async def broadcast(self, ctx, *args):
    if int(ctx.author.id) in [829374685480615946,299120006438846465,562608039224410112]:
      for guild in bot.guilds:
        for channel in guild.text_channels:
          if(channel.name in ["bot-testing","inorganic","inorganic-flashcards","anki","ankikopy","botspam","change-log","⋅inorganic-bot"]):
            try:
              await channel.send(" ".join(args[:]))
            except (discord.HTTPException, discord.Forbidden,AttributeError):
              continue
bot.add_cog(announce(bot))

bot.add_cog(NewDeck(bot))
bot.add_cog(invite(bot))
bot.add_cog(download(bot))
bot.add_cog(Quiz(bot))
bot.add_cog(serverinvite(bot))

#Spaced Repetition
import pickle
#pickle.dump(dict(),open("data.dat","wb"))
data=pickle.load(open("data.dat","rb"))

class SM2(commands.Cog):
  @commands.command(name="sm2")
  async def _work(self,message,session=""):
    questions=functions.questions("default")
    author=message.author.id
    channel=message.channel
    if author not in data or session=="reset":
      data[author]={"session":1,1:list(range(1,len(questions)))}
    elif session!="continue":
      data[author]["session"]+=1
    pickle.dump(data,open("data.dat","wb"))
    timeout_=135

    if author==562608039224410112:
      await message.send(data[author])

    order=list()
    for i in data[author]:
      if type(i)==int:
        if data[author]["session"]%i==0:
          order+=data[author][i]
    random.shuffle(order)

    correct, timeout, skipped, continoustimeout = dict(), 0, 0, 0
    
    if len(order)<1:
      done_embed=discord.Embed(title="Looks like your memory's so good that you have nothing for this session 🥳", description="Use the command again to proceed with the next session or $sm2 reset to reset progress",color=discord.Color.gold(),url="https://ncase.me/remember/")
      await message.send(embed=done_embed)
    for i in order:
      progress='\n' + str(round(sum(correct.values())/(len(questions)-1)*100,1)) + "% quiz completed"
      embed=discord.Embed(title=questions[i][0], color=discord.Color.blue(),url="",description=(questions[i][3]+progress))
      await channel.send(embed=embed)
          
      def funcc(x):

        return ((functions.format(x.content,questions[i][4]) == functions.format(questions[i][1],questions[i][4])) or (x.content == "quit") or (x.content == "skip") or (x.content=="stop")) and x.channel==channel and x.author.id==author

      try:
        global msg
        msg = await bot.wait_for('message', check=funcc,timeout=float(timeout_))


      except asyncio.TimeoutError:
        timeout += 1
        continoustimeout += 1
        if continoustimeout > 4:
          await channel.send("Stopping the quiz because the last 10 questions went unanswered.")
          await send_quit_embed_sm2(correct, skipped, timeout, channel)
          break
        await channel.send("Timeout!, The Answer was:")
        embed2 = discord.Embed(title="", color=discord.Color.red(),url="",description=questions[i][1])
        await channel.send(embed=embed2)
        if len(questions[i][2])>0:
          await channel.send(questions[i][2])
        for j in data[author]:
          if type(j)==int:
            if i in data[author][j]:
              data[author][j].remove(i)
        data[author][1].append(i)
        order.append(i)
        pickle.dump(data,open("data.dat","wb"))
        pass

      else:
        if msg.content == "quit" or msg.content=="stop":
          await channel.send('{.author} has stopped the quiz'.format(msg))
          
          await send_quit_embed_sm2(correct, skipped, timeout, channel)
          for j in data[author]:
            if type(j)==int:
              if i in data[author][j]:
                data[author][j].remove(i)
          data[author][1].append(i)
          break


        if msg.content == "skip":
          skipped += 1
          continoustimeout = 0
          skip_send = "Skipped!, The Answer was:"
          await channel.send(skip_send)
          embed2 = discord.Embed(title="", color=discord.Color.red(),url="",description=(questions[i][1]))
          await channel.send(embed=embed2)
          if len(questions[i][2])>0:
            await channel.send(questions[i][2])
          for j in data[author]:
            if type(j)==int:
              if i in data[author][j]:
                data[author][j].remove(i)
          data[author][1].append(i)
          order.append(i)
          continue
        
        else: 
          if msg.author in correct:
            correct[msg.author] += 1
          else:
            correct[msg.author]=1
          continoustimeout = 0
          s = '{.author} got the correct answer! \n' + questions[i][2] 
          await msg.channel.send(s.format(msg))
          if i==order[-1]:
                        
            await send_quit_embed_sm2(correct, skipped, timeout, channel)
            embed4=discord.Embed(title="Conquered this session!",color=discord.Color.gold(),url="https://www.youtube.com/watch?v=Utgrbq_CFt4",description="GGs!, You are dang OP")
            await channel.send(embed=embed4)
          for j in data[author]:
            if type(j)==int:
              if i in data[author][j]:
                pos=j
                break
          data[author][pos].remove(i)
          pos=(((8*pos + 1)**(1/2))-1)//(2)
          pos=((pos+1)*(pos+2))//2
          if pos not in data[author]:
            data[author][pos]=list()
          data[author][pos].append(i)
        pickle.dump(data,open("data.dat","wb"))

bot.add_cog(SM2(bot))
keep_alive()
bot.run(os.getenv("TOKEN"))