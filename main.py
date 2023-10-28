import bruhhbot
import strategy 
import tradebot
import asyncio

async def ask_for_strategies(available_strategies):
    print("Available strategies: ", ", ".join(available_strategies))
    choice = input("Which strats are you turning on today?: ")
    return choice.split(",")  # assuming comma-separated

async def main():
    bruhhbot = BruhhBot()
    stratbot = Strategy()

    all_strategies = bruhhbot.list_strategies() + stratbot.list_strategies()
    chosen_strategies = await ask_for_strategies(all_strategies)     

    # Validate chosen strategies
    for strat in chosen_strategies:
        if strat not in all_strategies:
            print(f"Strategy {strat} ain't valid.")
            return
    
    tradebot = tradebot.TradeBot(chosen_strategies)
    await tradebot.stratlistener() 
    stratbot.run(token)


if __name__ == '__main__':
    asyncio.run(main())




