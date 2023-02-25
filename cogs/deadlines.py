import datetime
import re
import discord
from discord.ext import commands, tasks

utc = datetime.timezone.utc

class Deadlines(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.check_loop.start() 
    
    @tasks.loop(time = datetime.time(hour=23, minute=0, second=0, tzinfo=utc))
    async def check_loop(self): 
        channel = self.client.get_channel(1075132101994745886) # Deadlines channel
        # channel = self.client.get_channel(922492279090995322) # Testchannel
        message1 = ""
        message3 = ""
        with open('deadlines.txt', 'r') as file:
            content = file.readlines()
        with open('deadlines.txt', 'w') as newfile:
            for i in range(len(content)):
                split_line = content[i].split('\t')
                date = split_line[0]
                name = split_line[1]
                date_time = datetime.datetime.strptime(date, "%d/%m/%Y")
                # Check if date has already passed
                if date_time >= datetime.datetime.now() - datetime.timedelta(days=1):
                    newfile.write(content[i])   
                    # Check if date is coming closer
                    if date_time <= datetime.datetime.now() + datetime.timedelta(days=1):
                        message1 += date + ': ' + name + '\n'
                    elif date_time <= datetime.datetime.now() + datetime.timedelta(days=7) and datetime.date.today().weekday() == 5:
                        message3 += date + ': ' + name + '\n'
        if message1 != None:
            embed1 = discord.Embed(title = "1 day left for upcoming deadlines", description=message1)
            await channel.send(embed = embed1)
        if message3 != None:
            embed3 = discord.Embed(title = "Upcoming deadlines for next week", description=message3)
            await channel.send(embed = embed3)

    @check_loop.before_loop
    async def before_printer(self):
        await self.client.wait_until_ready()

    def sort():
        with open('deadlines.txt', 'r') as file:
            content = file.readlines()
        text = []
        dates = []
        index = 0
        for line in content:
            split_line = line.split('\t')
            date = split_line[0].split('/')
            date.append(index)
            text.append(line)
            dates.append(date)
            index += 1
        dates.sort(key=lambda x:x[0])
        dates.sort(key=lambda x:x[1])
        dates.sort(key=lambda x:x[2])
        with open('deadlines.txt', 'w') as newfile:
            for index in dates:
                newfile.write(text[index[3]])

    @commands.command(usage="!adddate <date> <name>", 
                      description="Add date to list of deadlines", 
                      help="!adddate 15/02/2022 a very hard deadline\nDate should follow the format **DD/MM/YYYY**\nDate is allowed to contain **spaces**", 
                      aliases = ['ad'])
    async def adddate(self, ctx, date, *, name):
        if not re.match("[0-3][0-9]/[0-1][0-9]/[0-9]{4}", date):
            await ctx.send("Date has to be DD/MM/YYYY, try again.")
            return
        with open('deadlines.txt', 'a') as file:
            file.write(date + '\t')
            split_name = name.split(' ')
            for i in range(len(split_name)):
                file.write(split_name[i])
                if i != len(split_name) - 1:
                    file.write(' ')
                else:
                    file.write('\t')
            file.write('\n')
        Deadlines.sort()
        await ctx.send("Date added!")

    @commands.command(usage="!showdate <member>", 
                      description="Show current deadlines", 
                      help="!showdate: Show all deadlines", 
                      aliases = ['sd'])
    async def showdate(self, ctx):
        with open('deadlines.txt', 'r') as file:
            content = file.readlines()
        page = 1
        message = ''
        current_date = ''
        Deadlines.sort()
        if len(content) == 0:
            await ctx.send("No dates added yet!")
            return
        for line in content: 
            split_line = line.split('\t')
            if current_date != split_line[0]:
                current_date = split_line[0]
                if len(message) > 2000:
                    embed = discord.Embed(title = "Deadlines " + str(page), description = message)
                    await ctx.send(embed = embed)
                    message = ''
                    page += 1
                message += "**__" + current_date + ":__**\n"
            message += split_line[1] + '\n' 
        embed = discord.Embed(title = "Deadlines " + str(page), description = message)
        await ctx.send(embed = embed)

    @commands.command(usage="!deletedate <date> <name>", 
                      description="Delete date from deadlines", 
                      help="!deletedate 15/02/2022 a very hard deadline\nThe arguments have to be **the same arguments** as the ones in !adddate", 
                      aliases = ['dd'])
    async def deletedate(self, ctx, date, *, name):
        with open('deadlines.txt', 'r') as file:
            content = file.readlines()
        with open('deadlines.txt', 'w') as newfile:
            deleted = False
            for i in range(len(content)):
                split_line = content[i].split('\t')
                if split_line[0] == date and split_line[1] == name:
                    deleted = True
                    await ctx.send("Date has been deleted!")
                else:
                    newfile.write(content[i])   
            if not deleted:
                await ctx.send("No such date has been found!")

#Allows to connect cog to bot   
async def setup(client):
     await client.add_cog(Deadlines(client))