import websocket, json, pprint,talib, numpy


SOCKET = "wss://stream.binance.com:9443/ws/dogeusdt@kline_1m"
average_Price = []
closed_total = []
high_total = [] 
low_total = []
SSL_PERIOD =  5
STOCK = "DOGEUSD"
PAY = 100.00
POSTION = False
TRADE_QUANTITY = 0
rsi = None
atr  = None


def on_open(webS):
    print(" opened connection")
def on_close(webS):
    print(" closed connection")
def on_message(webS,message):
    print("received connection")
    json_message = json.loads(message)
    pprint.pprint(json_message)
    global closed_total
    candle = json_message["k"]
    final_value_tick = candle["x"]
    open_price = candle["o"]# Open price
    closed_price = candle["c"]#Close price
    high_price = candle["h"]#High price
    low_price = candle["l"]#Low price
    base_vol = candle["v"]#Base_asset_volume
    num_trades = candle["n"]#Number_of_trades
    quote_vol = candle["q"]#Quote_asset_volume
    taker_base = candle["V"]#Taker buy base asset volume
    taker_quote = candle["Q"]#Taker_buy_quote_asset_volume
     
    
        
        
    
    
    if final_value_tick:
        high_total.append(float(high_price))
        low_total.append(float(low_price))
        print("closed at this price {}".format(closed_price))
        closed_total.append(float(closed_price))
       
    
        
        
        if len(closed_total) > 5: 
            np_highs = numpy.array(high_total)
            np_lows = numpy.array(low_total)
            np_closes = numpy.array(closed_total)
            np_opens = numpy.array(float(open_price))
            avg = talib.AVGPRICE(float(open_price),np_highs,np_lows,5)
            rsi = talib.RSI(np_closes,5)
            atr = talib.ATR(np_highs,np_lows,np_closes,5) 
            print("all rsi calculated")
            print(rsi)
            print('---------')
            last_rsi = rsi[-1]
            print("The last rsi is {}".format(last_rsi))
            print('----')
            print(atr)
            last_atr = atr[-1]
            print('----')
            print("The last atr is {}".format(last_atr))
            print('----')
            average_Price.append(avg)
            print("Average price is {}",format(avg))
        
        
   
    print("-----")
    print(closed_total)
    
    
         
    
# def ema(webS):
#     day = 50
webS = websocket.WebSocketApp(SOCKET,on_open=on_open,on_close=on_close, on_message=on_message)

webS.run_forever()


