'''Objective is for tradebot to listen to the strategies in strategy.py
   -IF True then trigger the tradebot class lightitup methods
   -create option contract(s) order(s) using that strategy as the basis for variable passings
   - tweaking different ways to set the order (atm,otm,%ofbuyingpower,takeprofit%,stoploss%,etc)  '''

from webullbot import WebullBot
from strategy import Strategy 
from config import db
from datetime import datetime

class TradieBot:
    def __init__(self):
        self.wbbot = WebullBot()  # Instantiate WebullBot Class
        self.stratbot = Strategy()  # Instantiate the Strategy class


   def stratlistener(self, strategy_name):
    strategy_met, strat_data = getattr(self.stratbot, strategy_name)()
    if strategy_met:
        return True, strategy_name, strat_data
    return False, None, None

    class LightItUp:
        def __init__(self,wbbot):
            self.wbbot = wbbot

        def ingredients(self, stock, latest_price, expiration_date, strat_data):
            #AQUIRE THE INGREDIENTS: optionId,(optimal) lmtPrice, action, orderType, enforce,(optimal) quant
            # Initialize your variables here
                optionId = None
                lmtPrice = None
                action = 'BUY'
                orderType = 'LMT'
                enforce = 'GTC'
                optimal_strike = None
                optimal_lmtPrice = None 
                optimal_quant = 0
                ticker = strat_data['ticker']
                direction = strat_data['sentiment']
                expiration_date = strat_data['event_date']

            # Step 2: Calculate strikes,mids for LMTPRICE, and QUANT needed for creating contract order(s)
                strike_data = self.wbbot.wb_action.get_option_strikes(stock=ticker, expireDate=expiration_date, direction=direction)
                itm_strike = strike_data['itm_strike']
                otm_strikes = strike_data['otm_strikes']
                buying_power = float(self.wbbot.wb_check.get_account()['buyingPower'])
                trade_amount = 0.3 * buying_power

                # Loop through the strikes to find the optimal choice  
                ''' try setting a time condition so if its 0dte retrieve strikes differently'''
                
                for strike in [itm_strike] + otm_strikes:
                    option_data = self.wbbot.wb_action.get_strike_and_expdate(stock=ticker, expireDate=expiration_date, strike=str(strike), direction=direction)
                    mid_price = option_data.get('mid_price', 0)
                    optionId = option_data['option_data'].get('tickerId', None)
                                        
                    if mid_price == 0:
                        continue

                    # Calculate the maximum QUANT for this strike
                    possible_quant = int(trade_amount // (mid_price * 100))  # 100 is the option multiplier

                    if possible_quant > optimal_quant:
                        optimal_strike = strike
                        optimal_quant = possible_quant
                        optimal_lmtPrice = mid_price
                        optimal_optionId = option_data['option_data'].get('tickerId', None)  # Capture OptionId here

                # You now have the optimal_strike and optimal_quantity
                
                return {
                    'optionId': optimal_optionId,
                    'lmtPrice': optimal_lmtPrice,
                    'action': action,
                    'orderType': orderType,
                    'enforce': enforce,
                    'quant': optimalquant
                }

        def order(self, **kwargs):
            if 'optionId' in kwargs and 'lmtPrice' in kwargs:
                # Place the buy order first using indgredient variables
                self.wbbot.wb_action.start_order(**kwargs)
                print(f"Buy order placed for an optimal of {kwargs['quant']} contracts at limit price {kwargs['lmtPrice']}, with the opimtal Strike being: {kwargs['strike']}.")

                # Calculate the take-profit and stop-loss prices for sell order
                take_profit_price = kwargs['lmtPrice'] * 2  # +100%
                stop_loss_price = kwargs['lmtPrice'] * 0.65  # -35%

                # Initialize sell quantities list
                sell_quantities = []

                if kwargs['quant'] > 1:
                    if kwargs['quant'] > 2:
                        first_sell_quant = int(round(kwargs['quant'] * 2 / 3))
                    else:
                        first_sell_quant = kwargs['quant'] // 2

                    second_sell_quant = kwargs['quant'] - first_sell_quant
                    sell_quantities = [first_sell_quant, second_sell_quant]
                else:
                    sell_quantities = [1]

                # Place the first sell order
                self.wbbot.wb_action.start_order(
                    optionId=kwargs['optionId'],
                    lmtPrice=take_profit_price,
                    action='SELL',
                    orderType='STP LMT',
                    enforce=kwargs['enforce'],
                    quant=sell_quantities[0],
                    stpPrice=stop_loss_price
                )
                print(f"First sell order placed for {sell_quantities[0]} contracts at price {take_profit_price}, Strike: {kwargs['strike']}.")

                # Wait for the first sell order to be filled
                while True:
                    filled_orders = self.wbbot.wb_action.get_history_orders(status='Filled')
                    first_sell_order_filled = any(order['optionId'] == kwargs['optionId'] for order in filled_orders)
                    
                    if first_sell_order_filled:
                        break
                
                # Place the second sell order with adjusted take profit and stop loss
                final_take_profit_price = take_profit_price * 2  # +200%
                final_stop_loss_price = kwargs['lmtPrice']  # Break-even

                self.wbbot.wb_action.start_order(
                    optionId=kwargs['optionId'],
                    lmtPrice=final_take_profit_price,
                    action='SELL',
                    orderType='STP LMT',
                    enforce=kwargs['enforce'],
                    quant=sell_quantities[-1],
                    stpPrice=final_stop_loss_price
                )
                print(f"Final sell order placed for {sell_quantities[-1]} contracts at price {final_take_profit_price}, Strike: {kwargs['strike']}.")

            else:
                print("Couldn't place the order. Missing some data.")

                
# main function
async def main():
    trading_bot = TradieBot()
    strategy_list = ['rsitd9spx25', 'rsitd9spx13']  # Add new strategies here

    while True:
        for strat in strategy_list:
            strat_met, strat_name, strat_data = trading_bot.stratlistener(strat)
        
            if strat_met:
                ingredients = light_it_up.ingredients(strat_data)
                light_it_up.order(**ingredients)
        
        await asyncio.sleep(60)  # Sleep for 60 seconds

if __name__ == '__main__':
    asyncio.run(main())