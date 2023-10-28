import asyncpg
from datetime import datetime, time
import pytz  
import os
from dotenv import load_dotenv
load_dotenv()

class Fudstopdb:
    def __init__(self):
        pass

    async def connect(self):    
        #grabs the credential data for the postgresql database 
        self.conn = await asyncpg.connect(
            dbname=os.getenv('DB_NAME'),
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS')
            
        )

        self.dbconnect = True

    async def retrieve_dbdata(self, query):
        try:
            return await self.conn.fetch(query)
        except Exception as e:
            print(f"Error: {str(e)}")
            return []

    def checkdbconnect(self):

        if self.dbconnect:
            print("You are connected to the database.")
        else:
            print("Not connected to the database.")


class Strategy:
    def __init__(self):
        self.db = Fudstopdb()
    
    async def connect_db(self):
        await self.db.connect()

     def list_strategies(self):
        return [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__")]

    def format_price(self, price):
        #round up the prices to cents instead of having fuck ton of 0s
        if price >= 1000000:
            return f"${price / 1000000:.1f}M"
        elif price >= 1000:
            return f"${price / 1000:.1f}k"
        else:
            return f"${price:.2f}"

    async def flow(self):
        #strategy for flow of options within a range of over 30 days and over 100k 
        query = """
            SELECT strike, underlying_symbol, call_put, expiry, 
            SUM(size) as total_size, 
            SUM(price * size * 100) as total_price
            FROM option_equitytrade
            WHERE conditions = 'Intermarket Sweep Order'
                AND expiry >= current_date + 30
                AND expiry <= current_date + 100
            GROUP BY strike, call_put, underlying_symbol, expiry, trade_option_symbol, timestamp, conditions
            HAVING SUM(price * size * 100) >= 100000
            ORDER BY total_size DESC;
        """

        data = await self.db.retrieve_dbdata(query)

        if data:
            print(f"The following data meets the flow strategy:")
            for trade in data:
                strike, symbol, call_put, expiry, total_size, total_price = trade
                total_price = self.format_price(total_price)
                print(f"Strike: {strike}, Symbol: {symbol}, Type: {call_put}, Expiry: {expiry}, AggSize: {total_size}, AggPrice: {total_price}")
        else:
            print("No data found for flow strategy")
            
   

        data = self.db.retrieve_dbdata(query)

        if data:
            print(f"The following data meets the criteria for the test query strategy: {data}")
        else:
            print("No data found for the test queyr strategy")  

    async def rsitd9spx25(self):
        #listen for td9 2min and 5 min with extreme rsi during time zones (zones of time during the trade day where volume picksup)

        # Timezone and current time check
        est = pytz.timezone('US/Eastern')
        current_time = datetime.now(est).time()

        if not ((current_time >= time(10, 50) and current_time <= time(11, 20)) or \
                (current_time >= time(12, 50) and current_time <= time(13, 30))):
            return False, None
        query_2min = """
            SELECT 
            rsi.ticker,  
            rsi.sentiment,
            rsi.rsi_value AS rsi_2min,
            t9.td9_state AS td9_2min 
            FROM stock_rsi rsi
            LEFT JOIN td9_states t9 ON rsi.ticker = t9.ticker AND t9.timeframe = '2minute'
            WHERE
            rsi.timeframe = '2min'
            AND (rsi.rsi_value > 70 OR rsi.rsi_value < 30)
            AND ((t9.timeframe = '2minute' AND t9.td9_state = 'Setup Complete') OR t9.td9_state = 'Countdown Complete' OR t9.td9_state IS NULL);
            """
        data_2min = self.db.retrieve_dbdata(query_2min)

        query_5min = """
            SELECT 
            rsi.ticker,  
            rsi.rsi_value AS rsi_5min,
            rsi.sentiment,
            t9.td9_state AS t9_5min
            FROM stock_rsi rsi
            JOIN td9_states t9 ON rsi.ticker = t9.ticker
            WHERE
            rsi.timeframe = '5min'
            AND (rsi.rsi_value >= 67 OR rsi.rsi_value <= 33)
            AND ((t9.timeframe = '5minute' AND t9.td9_state = 'Setup Complete') OR t9.td9_state = 'Countdown Complete');
            """    
        data_5min = self.db.retrieve_dbdata(query_5min)

        if data_2min and data_5min:  # Check if both queries return data
            event_date = datetime.now().strftime('%Y-%m-%d')
            strat_data_25 = {
                'event_date': event_date,
                '2min_data': data_2min,
                '5min_data': data_5min,
            }
            print(strat_data_25)
            return True, strat_data_25
        else:
            return False, None

    def rsitd9spx13(self):
        pass 

    def checkdbconnect(self):
        self.db.checkdbconnect() 


  
  #def gexminmax presents the levels of the day #specific to gex , combo with rsi td9 gap lines might be the killer, dark pools as well,
  #a treasury strategy ? tlt ? 
  #if the 1hr 2 4hr or day rsi are at extremes warn before
  # trade presented, also check gap lines if GAP LINES (DAILY) is within 5 points of the rsitd9 boolean true then
  # wait until it reaches gap line to place order
  #yea next order of businesss is to setup the gap lines somehow to combine with the td9 and rsi