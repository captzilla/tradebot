import disnake
from disnake.ext import commands
from datetime import datetime, time
import pytz
from dotenv import load_dotenv
load_dotenv()


intents = disnake.Intents.all()

def list_strategies(self):
        return [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__")]

class BruhhBot(commands.Bot):
    
    def __init__(self, command_prefix, intents=intents):
        super().__init__(command_prefix, intents=intents)
        self.strategy_event = asyncio.Event()
        await self.strategy_event.set()

    def list_strategies(self):
        return [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__")]
    

    async def on_ready(self):
        print(f"Bot is ready! Logged in as {self.user.name}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        channel_name = message.channel.name
        if channel_name == "strategy_channel":
            # Check if the message has embeds
            if message.embeds:
                embed = message.embeds[0]  # Take the first embed
                
                # Run your flow strategy check
                if self.check_flow():
                    await self.strategy_event.set()
                    await message.channel.send("Flow strategy triggered. Time to trade:")
                    
                # Check for 'SPX' or 'SPY' ticker only in the rsitd9spx25 strategy
                if any(ticker in (embed.title or "") or ticker in (embed.description or "") for ticker in ["SPX", "SPY"]):
                    if self.check_rsitd9spx25():
                        self.strategy_event.set()
                        await message.channel.send("rsitd9spx25 strategy triggered. Time to trade.")


                
    def check_flow(self):
        # Your flow strategy logic here
    return {True,'ticker': '','sentiment': '','event_date': ''}

    def check_rsitd9spx25(self):
        est = pytz.timezone('US/Eastern')
        current_time = datetime.now(est).time()
        if not ((current_time >= time(10, 50) and current_time <= time(11, 20)) or \
                (current_time >= time(12, 50) and current_time <= time(13, 30))):
            return False
        # Your strategy logic here
        return (True, 'rsitd9spx25', {'ticker': '', 'sentiment': '', 'event_date': ''})

#mybot = BruhhBot(command_prefix="!", intents=intents)
token = os.getenv('TOKEN')