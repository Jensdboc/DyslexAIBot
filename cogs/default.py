from discord.ext import commands

class Default(commands.Cog):

    def __init__(self, client):
        self.client = client  

    # @commands.command(usage="!poll", 
    #                   description="Poll command", 
    #                   help="")
    # async def poll(self, ctx, *, question):
    #     await ctx.send(question)  
    
#Allows to connect cog to bot   
async def setup(client):
    await client.add_cog(Default(client))
