from discord.ext import commands

class Default(commands.Cog):

    def __init__(self, client):
        self.client = client  

#Allows to connect cog to bot   
async def setup(client):
    await client.add_cog(Default(client))
