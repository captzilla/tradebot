import bruhhbot
import tradebot
import asyncio

async def main():
    token = bot.token
    # Create an instance of the classes
    stratbot = bot.BruhhBot(command_prefix="!", intents=intents)
    tradebot = TradeBot(stratbot)
    await tradebot.stratwait()

    stratbot.run(token)


if __name__ == '__main__':
    asyncio.run(main())




