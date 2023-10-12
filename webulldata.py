

from config import user_data
from webullendpoints import urls
from webull import webull, paper_webull


class WebullData:
    
    def __init__(self):
         
        self.username = input("Enter your username: ")
        
        if self.username.endswith("-real"):
            self.account_type = "real"
            self.username = self.username[:-6]  # Remove the "-real" suffix
        else:
            self.account_type = "paper"

        if self.account_type == "paper":
            self.wb = paper_webull()
            print("creating paper webull class")
        elif self.account_type == "real":
            self.wb = webull()
            print("creating real webull")
        else:
            print("Invalid account type. Please enter 'paper' or 'real'.")
            return

        
        self.wb._acct_id = user_data[self.username].get("account_id")
        self.wb._paper_acct_id = user_data[self.username].get("paper_acct_id")      
        self.wb._access_token = user_data[self.username].get("access_token")
        self.wb._trade_token = user_data[self.username].get("trade_token")
        self.wb._trade_pin = user_data[self.username].get("trade_pin")
        self.wb._token_expire = user_data[self.username].get("token_expire")
        self.wb._usr = user_data[self.username].get("login_usr")
        self.wb._pwd = user_data[self.username].get("login_pwd")  
        
        self.headers = self.wb.build_req_headers()
        #print(self.headers) #  if needed to check headers 

"""
    class AccountSummary:
        def __init__(self, data):
            self.sec_account_id = data.get('secAccountId')
            self.broker_id = data.get('brokerId')
            self.account_type = data.get('accountType')
            self.account_type_name = data.get('accountTypeName')
            self.account_number = data.get('accountNumber')
            self.currency = data.get('currency')
            self.net_liquidation_value = data.get('netLiquidationValue')
            self.total_market_value = data.get('totalMarketValue')
            self.total_cash_value = data.get('totalCashValue')
            self.day_buying_power = data.get('dayBuyingPower')
            self.overnight_buying_power = data.get('overnightBuyingPower')
            self.day_trade_counts = data.get('dayTradeCounts', [])
            self.unrealized_profit_loss = data.get('unrealizedProfitLoss')
            self.unrealized_profit_loss_rate = data.get('unrealizedProfitLossRate')
            self.asset_ratio_list = data.get('assetRatioList', [])
            self.settled_funds = data.get('settledFunds')
            self.unsettled_funds = data.get('unsettledFunds')
            self.available_withdraw = data.get('availableWithdraw')
            self.incoming_funds = data.get('incomingFunds')
            self.maint_margin = data.get('maintMargin')
            self.init_margin = data.get('initMargin')
            self.risk_info = data.get('riskInfo', {})
            self.is_pdt = data.get('isPdt')
            self.option_trade_level = data.get('optionTradeLevel')
            self.allow_change = data.get('allowChange')
            self.type_change_status = data.get('typeChangeStatus')
            self.day_trades_remaining = data.get('dayTradesRemaining')
            self.accrued_interest = data.get('accruedInterest')
            self.accrued_dividend = data.get('accruedDividend')
            self.accrued_total = data.get('accruedTotal')
            self.to_receive_interest = data.get('toReceiveInterest')
            self.to_receive_dividend = data.get('toReceiveDividend')
            self.to_receive_total = data.get('toReceiveTotal')
            self.long_market_value = data.get('longMarketValue')
            self.short_market_value = data.get('shortMarketValue')
            self.option_bp = data.get('optionBp')
            self.credit_bp = data.get('creditBp')
            self.crypto_bp = data.get('cryptoBp')
            self.restriction_result = data.get('restrictionResult')

    class AssetSummary:
        def __init__(self, data):
            capital = data.get('capital', {})
            self.account_type = capital.get('accountType')
            self.currency = capital.get('currency')
            self.net_liquidation_value = capital.get('netLiquidationValue')
            self.unrealized_profit_loss = capital.get('unrealizedProfitLoss')
            self.unrealized_profit_loss_rate = capital.get('unrealizedProfitLossRate')
            self.unrealized_profit_loss_base = capital.get('unrealizedProfitLossBase')
            self.day_buying_power = capital.get('dayBuyingPower')
            self.overnight_buying_power = capital.get('overnightBuyingPower')
            self.settled_funds = capital.get('settledFunds')
            self.unsettled_funds = capital.get('unsettleFunds')
            self.crypto_buying_power = capital.get('cryptoBuyingPower')
            self.option_buying_power = capital.get('optionBuyingPower')
            self.total_cash_value = capital.get('totalCashValue')
            self.total_cost = capital.get('totalCost')
            self.remain_trade_times = capital.get('remainTradeTimes')
            self.total_market_value = capital.get('totalMarketValue')
            self.pending_funds = capital.get('pendingFunds')
            self.available_buying_power = capital.get('availableBuyingPower')
            self.unavailable_buying_power = capital.get('unAvailableBuyingPower')
            self.credit_diff_bp = capital.get('creditDiffBp')
            self.credit_bp = capital.get('creditBp')
            self.frozen_bp = capital.get('frozenBp')
            self.unrecovered_bp = capital.get('unRecoveredBp')
            self.crypto_bp = capital.get('cryptoBp')
            self.positions = [Position(item) for item in data.get('positions', [])]

    class Position: #nested within capital that is nested in assetsummary
        def __init__(self, data):
            self.id = data.get('id')
            self.ticker_type = data.get('tickerType')
            self.option_strategy = data.get('optionStrategy')
            items = data.get('items', [])
            if items:
                item = items[0]
                ticker = item.get('ticker', {})
                self.ticker_id = ticker.get('tickerId')
                self.exchange_id = ticker.get('exchangeId')
                self.type = ticker.get('type')
                self.sec_type = ticker.get('secType')
                self.region_id = ticker.get('regionId')
                self.region_code = ticker.get('regionCode')
                self.currency_id = ticker.get('currencyId')
                self.currency_code = ticker.get('currencyCode')
                self.name = ticker.get('name')
                self.symbol = ticker.get('symbol')
                self.dis_symbol = ticker.get('disSymbol')
                self.dis_exchange_code = ticker.get('disExchangeCode')
                self.exchange_code = ticker.get('exchangeCode')
                self.list_status = ticker.get('listStatus')
                self.template = ticker.get('template')
                self.exchange_trade = ticker.get('exchangeTrade')
                self.derivative_support = ticker.get('derivativeSupport')
                self.futures_support = ticker.get('futuresSupport')
                self.tiny_name = ticker.get('tinyName')
                self.is_ptp = ticker.get('isPTP')
                self.asset_type = ticker.get('assetType')
                self.action = item.get('action')
                self.quantity = item.get('quantity')
                self.option_type = item.get('optionType')
                self.option_expire_date = item.get('optionExpireDate')
                self.option_exercise_price = item.get('optionExercisePrice')
                self.option_contract_multiplier = item.get('optionContractMultiplier')
                self.option_contract_deliverable = item.get('optionContractDeliverable')
                self.last_price = item.get('lastPrice')
                self.belong_trade_price = item.get('belongTradePrice')
                self.cost_price = item.get('costPrice')
                self.total_cost = item.get('totalCost')
                self.currency = item.get('currency')
                self.market_value = item.get('marketValue')
                self.unrealized_profit_loss = item.get('unrealizedProfitLoss')
                self.unrealized_profit_loss_rate = item.get('unrealizedProfitLossRate')
                self.unrealized_profit_loss_base = item.get('unrealizedProfitLossBase')
                self.proportion = item.get('proportion')
                self.option_cycle = item.get('optionCycle')
                self.update_position_time = item.get('updatePositionTime')
                self.option_can_exercise = item.get('optionCanExercise')
                self.recently_expire_flag = item.get('recentlyExpireFlag')
                self.remain_day = item.get('remainDay')
                self.is_lending = item.get('isLending')
                self.can_fract = item.get('canFract')
                self.am_or_pm = item.get('amOrPm')
                self.expiration_type = item.get('expirationType')

    # Usage:

    # Assuming 'data' is your JSON data
    account_summary_data = data.get('accountSummaryVO', {})
    asset_summary_data = data.get('assetSummaryVO', {})

    account_summary = AccountSummary(account_summary_data)
    asset_summary = AssetSummary(asset_summary_data)

    # Now you can access the attributes like this:
    print(account_summary.account_type)
    print(asset_summary.positions[0].symbol)''' 

class QueryDerivatives:
        def __init__(self, option_data):
            self.open = option_data.get('open')
            self.high = option_data.get('high')
            self.low = option_data.get('low')
            self.strikePrice = option_data.get('strikePrice')
            self.isStdSettle = option_data.get('isStdSettle')
            self.preClose = option_data.get('preClose')
            self.openInterest = option_data.get('openInterest')
            self.volume = option_data.get('volume')
            self.latestPriceVol = option_data.get('latestPriceVol')
            self.delta = option_data.get('delta')
            self.vega = option_data.get('vega')
            self.impVol = option_data.get('impVol')
            self.gamma = option_data.get('gamma')
            self.theta = option_data.get('theta')
            self.rho = option_data.get('rho')
            self.close = option_data.get('close')
            self.change = option_data.get('change')
            self.changeRatio = option_data.get('changeRatio')
            self.expireDate = option_data.get('expireDate')
            self.tickerId = option_data.get('tickerId')
            self.belongTickerId = option_data.get('belongTickerId')
            self.openIntChange = option_data.get('openIntChange')
            self.activeLevel = option_data.get('activeLevel')
            self.cycle = option_data.get('cycle')
            self.weekly = option_data.get('weekly')
            self.executionType = option_data.get('executionType')
            self.direction = option_data.get('direction')
            self.derivativeStatus = option_data.get('derivativeStatus')
            self.currencyId = option_data.get('currencyId')
            self.regionId = option_data.get('regionId')
            self.exchangeId = option_data.get('exchangeId')
            self.symbol = option_data.get('symbol')
            self.unSymbol = option_data.get('unSymbol')
            self.askList = option_data.get('askList')
            self.bidList = option_data.get('bidList')
            self.quoteMultiplier = option_data.get('quoteMultiplier')
            self.quoteLotSize = option_data.get('quoteLotSize')
            self.tradeTime = option_data.get('tradeTime')
            self.timeZone = option_data.get('timeZone')
            self.tzName = option_data.get('tzName')
            self.tradeStatus = option_data.get('tradeStatus')
            self.tradeStamp = option_data.get('tradeStamp')

    class Ticker:
                def __init__(self, ticker_data):
                    self.tickerId = ticker_data.get('tickerId')
                    self.exchangeId = ticker_data.get('exchangeId')
                    self.type = ticker_data.get('type')
                    self.regionId = ticker_data.get('regionId')
                    self.regionCode = ticker_data.get('regionCode')
                    self.currencyId = ticker_data.get('currencyId')
                    self.symbol = ticker_data.get('symbol')
                    self.disSymbol = ticker_data.get('disSymbol')
                    self.disExchangeCode = ticker_data.get('disExchangeCode')
                    self.exchangeCode = ticker_data.get('exchangeCode')
                    self.listStatus = ticker_data.get('listStatus')
                    self.subType = ticker_data.get('subType')

    class Position:
            def __init__(self, id, accountId, paperId, ticker, status, position, cost, costPrice, lastPrice, marketValue,
                        unrealizedProfitLoss, unrealizedProfitLossRate, tickerType, optionType, optionExpireDate,
                        optionContractMultiplier, optionExercisePrice, belongTickerId):
                self.id = id
                self.accountId = accountId
                self.paperId = paperId
                self.ticker = ticker
                self.status = status
                self.position = position
                self.cost = cost
                self.costPrice = costPrice
                self.lastPrice = lastPrice
                self.marketValue = marketValue
                self.unrealizedProfitLoss = unrealizedProfitLoss
                self.unrealizedProfitLossRate = unrealizedProfitLossRate
                self.tickerType = tickerType
                self.optionType = optionType
                self.optionExpireDate = optionExpireDate
                self.optionContractMultiplier = optionContractMultiplier
                self.optionExercisePrice = optionExercisePrice
                self.belongTickerId = belongTickerId




            def calculate_itm_strike(self, options, latest_price, direction):
                if direction == 'call':
                    # For calls, ITM strike is the equal or lower price closest to the latest price
                    itm_strike = max(option['strikePrice'] for option in options if float(option['strikePrice']) <= latest_price)
                else:
                    # For puts, ITM strike is the equal or higher price closest to the latest price
                    itm_strike = min(option['strikePrice'] for option in options if float(option['strikePrice']) >= latest_price)
                
                return itm_strike

 

 """ 
