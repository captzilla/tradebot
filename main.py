

import requests
import disnake 
from disnake.ext import commands, tasks
#from thotbot.bot import ThotBot, intents
#from config import token
from cmds.strategy import Strategy
import webulldata
import webullbot
import webull

# Create an instance of the classes
stratbot = Strategy()
tradebot = TradeBot()
wbbot = WebullBot()

# Call the method to check the database connection
stratbot.checkdbconnect()
stratbot.flow()
stratbot.rsitd9spx25()

#wbbot.check_real_acct()
#bot = MyBot(command_prefix="!", intents=intents)


#bot.load_extension("cmds.general")
#bot.run(token)



