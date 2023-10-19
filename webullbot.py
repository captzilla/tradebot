# objective is to get the webull paper and real acct
# and use the webull endpoint urls
#  in webull to 
#aquire the webull order info as well as best as can be done
#also gotta modify the webullsdk if necessary to include
#endpoints for all of this logic if its not there.

import os
import json
import requests
from typing import List
import aiohttp
import asyncio
from  webull import webull, paper_webull
from dotenv import load_dotenv
load_dotenv()

class WebullBot:
    def __init__(self):
        self.webullcheck = self.WebullCheck(self) 
        self.webullaction = self.WebullAction(self)

        self.username = input("Enter your username: ")

        if self.username.endswith("-real"):
            self.account_type = "real"
            self.username = self.username[:-6]  # Remove the "-real" suffix
        else:
            self.account_type = "paper"

        if self.account_type == "paper":
            self.wb = paper_webull()
            print("Creating paper webull class")
        elif self.account_type == "real":
            self.wb = webull()
            print("Creating real webull class")
        else:
            print("Invalid account type. Please enter 'paper' or ' real'.")
            return

        #get the user data from .env file which houses the sensitive info
        user_data_str = os.getenv("USER_DATA")
        self.user_data = json.loads(user_data_str) if user_data_str else {}

        self.wb._acct_id = self.user_data.get(self.username, {}).get("account_id")
        self.wb._paper_acct_id = self.user_data.get(self.username, {}).get("paper_acct_id")      
        self.wb._access_token = self.user_data.get(self.username, {}).get("access_token")
        self.wb._trade_token = self.user_data.get(self.username, {}).get("trade_token")
        self.wb._trade_pin = self.user_data.get(self.username, {}).get("trade_pin")
        self.wb._token_expire = self.user_data.get(self.username, {}).get("token_expire")
        self.wb._usr = self.user_data.get(self.username, {}).get("login_usr")
        self.wb._pwd = self.user_data.get(self.username, {}).get("login_pwd")  

        self.headers = self.wb.build_req_headers()
        #print(self.headers) #  if needed to check headers     
 
    def checkauth(self):
        # First, we check that trade token.
        trade_token_check = self.wb.get_trade_token(self.wb._trade_pin)
        print("Authentication: ", trade_token_check)

        '''# If it ain't right, we gotta dive deeper.
        if not trade_token_check:
            # Check if access token's gone bad.
            access_token_status = self.wb.refresh_login()
            print(access_token_status)
            if 'access_token' not in access_token_status:
                print("Yo, your access token's messed up!")

            # Now we check that trade token.
            trade_token_status = self.wb.refresh_trade_token(self.wb._trade_pin)
            if 'trade_token' not in trade_token_status:
                print("Man, that trade token ain't right either!")
         HAVE TO RETRIEVE ACCESS AND TRADE TOKENS WON'T WORK(...YET)'''
       

    class WebullCheck:
        def __init__(self, bot) :
            self.bot = bot

        def acctstatus(self):
            check_account_status = input("Do you want to check account status? (yes/no): ").strip().lower()
            if check_account_status == "yes":    
                if hasattr(self.bot, 'account_type'):  
                    if self.bot.account_type == "paper":  
                        print(self.bot.wb.get_account(paper_acct_id=self.bot.wb._paper_acct_id))
                    elif self.bot.account_type == "real":  
                        print(self.bot.wb.get_account_id(), self.bot.wb.get_account())
                                  
        def mypositions(self):
            check_positions = input("Do you want to check positions? (yes/no): ").strip().lower()
            if check_positions == "yes":
                if hasattr(self.bot, 'account_type'): 
                    if self.bot.account_type == "paper":
                        account_info = self.bot.wb.get_account(paper_acct_id=self.wb._paper_acct_id)  
                        print(account_info['positions']) 
                    elif self.bot.account_type == "real":
                        print(self.bot.wb.get_positions()) 

        def my_history_orders(self,status=None, count=None):
            if hasattr(self.bot, 'account_type'): 
                if self.bot.account_type == "paper":
                    history_order = self.bot.wb.get_history_orders(status=status, count=count) 
                    print(history_order)
                elif self.bot.account_type == "real": 
                    history_order = self.bot.wb.get_history_orders(status=status, count=count)
                    print(history_order) 

    class WebullAction:
        def __init__(self, bot) :
            self.bot = bot
    
        def get_option_strikes(self, stock, expireDate, direction, num_otm=3, include_itm=True):
            options = self.bot.wb.get_options(stock=stock, expireDate=expireDate, direction=direction)
            available_strikes = sorted([float(option['strikePrice']) for option in options])

            #print(f"Available Strikes: {available_strikes}")  # Debugging line

            quote = self.bot.wb.get_quote(stock=stock)
            latest_price = float(quote['close'])
            print(f"Latest Price for {stock}: {latest_price}")

            if not available_strikes or latest_price is None:
                return {'error': 'Invalid data'}

            if direction == 'call':
                itm_strike = max([strike for strike in available_strikes if strike < latest_price])
                otm_strikes = ([strike for strike in available_strikes if strike > itm_strike])[:num_otm]
            else:  # This is for 'put' options
                itm_strike = min([strike for strike in available_strikes if strike > latest_price])
                otm_strikes = sorted([strike for strike in available_strikes if strike < itm_strike], reverse=True)[:num_otm]

            result = {'itm_strike': itm_strike, 'otm_strikes': otm_strikes} if include_itm else {'otm_strikes': otm_strikes}
            return result
            
        def get_strike_and_expdate(self, stock, expireDate, strike, direction):
            #Gets latest price of symbol, strike and expdate and its details into option_data 
            quote = self.bot.wb.get_quote(stock=stock)
            latest_price = float(quote['close'])
            print(f"Latest Price for {stock}: {latest_price}")
        
            # Get options for the specified expiration date and stock
            options =  self.bot.wb.get_options_by_strike_and_expire_date(stock=stock,
                        expireDate=expireDate, strike=strike, direction=direction)

            option_data = options[0][direction] if options and direction in options[0] else None 
            if not option_data:
                return {'error': 'No option data found'}
        
            optionId = option_data['tickerId'] if option_data else None
            if optionId:
                option_quote_data = self.bot.wb.get_option_quote(stock=stock, optionId=optionId)
                #print("Option Quote Data: ", option_quote_data) debugging 

                # Merge the dictionaries
            if option_quote_data:
                option_data.update(option_quote_data[0])
            
            def get_mid_price(data):
                #print(f"Data in get_mid_price: {data}") debugging
                try:
                    bid_price = float(data['bidList'][0]['price'])
                    ask_price = float(data['askList'][0]['price'])
                    return round((bid_price + ask_price) / 2, 2)
                except KeyError:
                    print(f"KeyError occurred. Data keys are: {data.keys()}")

            mid_price = get_mid_price(option_data)

            print(f'Strike provided: {strike} Expiring: {expireDate}')
            # Filter options with matching strikePrice only neeed if multiple strike prices ?
            #matching_options = [option for option in options if option['strikePrice'] == str(strike)] 
            #print(matching_options)
            
            
            return {'option_data': option_data, 'mid_price': mid_price}
            

        def start_order(self, optionId, lmtPrice, stpPrice, action, orderType,enforce,quant):
            if hasattr(self.bot, 'account_type'):
                if self.bot.account_type == "paper":
                    self.bot.wb.place_option_order(optionId=optionId,lmtPrice=lmtPrice,
                    action=action, orderType=orderType,enforce=enforce, quant=quant)
                    

                elif self.account_type == "real":
                    self.bot.wb.place_option_order(optionId=optionId,lmtPrice=lmtPrice,
                    stpPrice=None, action=action, orderType=orderType, quant=quant)

                    return self.bot.wb.openorder() 

                    
        def get_activities(self):
            pass # I wll use this for analyzing the trades  I made for improvements 
            #using the data      
                

    async def main(self):
        self.checkauth()
        #self.webullcheck.acctstatus()
        
        #strike_and_expdate_options = self.wb_action.get_strike_and_expdate(stock="spy", expireDate="2023-10-13", strike='427',direction='call')
        #print(strike_and_expdate_options)
        #strikes = self.wb_action.get_option_strikes(stock="SPY", expireDate="2023-10-13", direction="all")
        #print(strikes)
        #self.wb_action.start_order(optionId='1041084779', lmtPrice=.01,stpPrice=None, action='BUY', orderType='LMT', enforce='GTC', quant=1)
        #it worked for real , now paper test time 

        
        #history_orders = self.wb_check.my_history_orders(status='ALL', count=30)
        #for order in history_orders:
        #    print(order)


if __name__ == '__main__':
  
    webullbot = WebullBot()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(webullbot.main())


