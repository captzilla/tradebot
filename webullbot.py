# objective is to get the webull paper and real acct
# and use the webull endpoint urls
#  in webull to 
#aquire the webull order info as well as best as can be done
#also gotta modify the webullsdk if necessary to include
#endpoints for all of this if its not there.

import json
import requests
from typing import List
import aiohttp
import asyncio
from webulldata import WebullData

class WebullBot:
    def __init__(self):
        self.wbdata = WebullData()

        # Access the account type and other attributes from wbdata
        self.account_type = self.wbdata.account_type
        self.wb = self.wbdata.wb
        self.headers = self.wbdata.headers
        #print(self.headers)

        self.wb_check = self.WebullCheck(self.wbdata)
        self.wb_action = self.WebullAction(self.wbdata)
    def checkauth(self):
        print(self.wbdata.wb.get_trade_token(self.wbdata.wb._trade_pin))  
        #if false check accesstoken,tradetoken,in config, these reset after logout 
   
    class WebullCheck:
        def __init__(self, wbdata):
            self.wbdata = wbdata

        def acctstatus(self):
            if hasattr(self.wbdata, 'account_type'):  
                if self.wbdata.account_type == "paper":  
                    self.wbdata.wb.get_account(paper_acct_id=self.wbdata.wb._paper_acct_id)

                elif self.wbdata.account_type == "real":  
                    self.wbdata.wb.get_account_id()  
                    self.wbdata.wb.get_account()  

                else:
                    print("Yo dawg thats not an existing acct type: try again")
        
        def mypositions(self):
            if hasattr(self.wbdata, 'account_type'): 
                if self.wbdata.account_type == "paper":
                    account_info = self.wbdata.wb.get_account(paper_acct_id=self.wbdata.wb._paper_acct_id)  
                    return account_info['positions'] 
                elif self.wbdata.account_type == "real":
                    return self.wbdata.wb.get_positions() 

        def my_history_orders(self,status=None, count=None):
            if hasattr(self.wbdata, 'account_type'): 
                if self.wbdata.account_type == "paper":
                   history_order = self.wbdata.wb.get_history_orders(status=status, count=count) 
                   return history_order
                elif self.wbdata.account_type == "real": 
                    history_order = self.wbdata.wb.get_history_orders(status=status, count=count)
                return history_order 

    class WebullAction:
        def __init__(self, wbdata):
            self.wbdata = wbdata
      
        def get_option_strikes(self, stock, expireDate, direction, num_otm=3, include_itm=True):
            options = self.wbdata.wb.get_options(stock=stock, expireDate=expireDate, direction=direction)
            available_strikes = sorted([float(option['strikePrice']) for option in options])

            #print(f"Available Strikes: {available_strikes}")  # Debugging line

            quote = self.wbdata.wb.get_quote(stock=stock)
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
            quote = self.wbdata.wb.get_quote(stock=stock)
            latest_price = float(quote['close'])
            print(f"Latest Price for {stock}: {latest_price}")
           
            # Get options for the specified expiration date and stock
            options =  self.wbdata.wb.get_options_by_strike_and_expire_date(stock=stock,
                         expireDate=expireDate, strike=strike, direction=direction)

            option_data = options[0][direction] if options and direction in options[0] else None 
            if not option_data:
                return {'error': 'No option data found'}
           
            optionId = option_data['tickerId'] if option_data else None
            if optionId:
                option_quote_data = self.wbdata.wb.get_option_quote(stock=stock, optionId=optionId)
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
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                
            '''#Get the expiration dates (1 DTE and 0 DTE)
                
                expiration_dates = self.wbdata.wb.get_options(stock=stock, count=count,expireDate=expireDate)
                #print(f'API RESPONSE: {expiration_dates}')
                
                call_expire_dates = set(entry['call']['expireDate'] for entry in expiration_dates if 'call' in entry)
                put_expire_dates = set(entry['put']['expireDate'] for entry in expiration_dates if 'put' in entry)
                
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Combine and return the unique expiration dates
                unique_dates = call_expire_dates.union(put_expire_dates)
                print(f'Unique Expiration Dates: {unique_dates}')

                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                #Get the options for the expiration dates
                options = []
                for date in expiration_dates:
                    if 'call' in date:
                        options.append(date['call'])
                    if 'put' in date:
                        options.append(date['put'])
                return options'''

        def start_order(self, optionId, lmtPrice, stpPrice, action, orderType,enforce,quant):
            if hasattr(self.wbdata, 'account_type'):
                if self.wbdata.account_type == "paper":
                    self.wbdata.wb.place_option_order(optionId=optionId,lmtPrice=lmtPrice,
                    action=action, orderType=orderType,enforce=enforce, quant=quant)
                    

                elif self.wbdata.account_type == "real":
                    self.wbdata.wb.place_option_order(optionId=optionId,lmtPrice=lmtPrice,
                    stpPrice=None, action=action, orderType=orderType, quant=quant)

                    return self.wbdata.wb.openorder() 

                     
        def get_activities(self):
            pass # I wll use this for analyzing the trades  I made for improvements 
            #using the data      
           

    async def main(self):
        self.checkauth()
        #self.wb_check.acctstatus()
        #self.wb_check.mypositions()
        #strike_and_expdate_options = self.wb_action.get_strike_and_expdate(stock="spy", expireDate="2023-10-13", strike='427',direction='call')
        #print(strike_and_expdate_options)
        #strikes = self.wb_action.get_option_strikes(stock="SPY", expireDate="2023-10-13", direction="all")
        #print(strikes)
        self.wb_action.start_order(optionId='1041084779', lmtPrice=.01,stpPrice=None, action='BUY', orderType='LMT', enforce='GTC', quant=1)
        #it worked for real , now paper test time 

        
        #history_orders = self.wb_check.my_history_orders(status='ALL', count=30)
        #for order in history_orders:
        #    print(order)


if __name__ == '__main__':
  
    webullbot = WebullBot()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(webullbot.main())


