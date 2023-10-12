import disnake
from disnake.ext import commands

intents = disnake.Intents.all()

class ThotBot(commands.Bot):
    def __init__(self, command_prefix, intents=intents):
        super().__init__(command_prefix, intents=intents)
        
    async def on_ready(self):
        print(f"Bot is ready! Logged in as {self.user.name}")
       
   
    async def on_message(self, message):
        if message.author == self.user:
            return

        await self.process_commands(message)

    
#this was in genearl.py 
# mybot = MyBot(command_prefix="!", intents=intents)

#class General(commands.Cog):
#    def __init__(self, bot):
#        self.bot = bot
#        self.print_recent.start()  # start the task loop when this cog is loaded
        
#    @commands.slash_command()
#    async def general(self, interaction):
#        pass

#    @general.sub_command()
#    async def yao(interaction: disnake.ApplicationCommandInteraction):
#        """Says hello in chat."""
#        embed = Embed(
#            title="Yao wats good!",
#            description="Yao! Welcome back bruh.",
#        )
#        await interaction.send(embed=embed)

#def setup(bot: commands.Bot):
#    bot.add_cog(General(bot))
#    print(f"General commands have been loaded!")
