import websocket, json, pprint,talib, numpy

def bot(STOCK):
    STOCK = STOCK.upper()
    SOCKET = "wss://stream.binance.com:9443/ws/{}usdt@kline_1m".format(STOCK.lower())
    avg = 0 
    open_total = []
    closed_total = []
    high_total = [] 
    low_total = []
    SSL_PERIOD =  14
    rsi_high = 70
    rsi_low = 30 
    adx_high = 20
    adx_low = 15
    PAY = 100.00
    POSTION = False
    TRADE_QUANTITY = 0
    profit = 0
    # MAX = max(high_total)
    # LOW = min(low_total)


    def on_open(webS):
        print(" opened connection")
    def on_close(webS):
        print(" closed connection")
    def on_message(webS,message):
        print("received connection")
        json_message = json.loads(message)
        # pprint.pprint(json_message)
        # global closed_total
    
        
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
            open_total.append(float(open_price))
            high_total.append(float(high_price))
            low_total.append(float(low_price))
            closed_total.append(float(closed_price))
            # print("Open: {}".format(open_price))
            # print('------')
            # print("High: {}".format(high_price))
            # print('------')
            # print("Low: {}".format(low_price))
            # print('------')
            # print("closed at this price {}".format(closed_price))
            
        
        
        
            
            
            if len(closed_total) > SSL_PERIOD:
                
                np_highs = numpy.array(high_total)
                np_lows = numpy.array(low_total)
                np_closes = numpy.array(closed_total)
                np_opens = numpy.array(open_total)
                rsi = talib.RSI(np_closes,SSL_PERIOD)
                atr = talib.ATR(np_highs,np_lows,np_closes,SSL_PERIOD) 
                avg = talib.AVGPRICE(np_opens,np_highs,np_lows,np_closes)
                ema = talib.EMA(np_closes,SSL_PERIOD)
                dp = talib.PLUS_DM(np_highs,np_lows,SSL_PERIOD)
                dm = talib.MINUS_DM(np_highs,np_lows,SSL_PERIOD)
                adx = talib.ADX(np_highs,np_lows,np_closes,SSL_PERIOD)
                ema += atr
                # print('---------')
                # print("The last rsi is {}".format(rsi[-1]))
                # print('----')
                # print("The last atr is {}".format(atr[-1]))
                # print('----')
                # print("last Average price is {}".format(avg[-1]))
                # print('----')
                # print("last  true EMA  is {}".format(ema[-1]))
                # print('----')
                # print("last DMI+  is {}".format(dp[-1]))
                # print('----')
                # print("last DMI-  is {}".format(dm[-1]))
                # print('----')
                # print("last ADX-  is {}".format(adx[-1]))
                # print('--RSI--')
                # print(rsi)
                # print('--ATR--')
                # print(atr)
                # print('--AVG--')
                # print(avg)
                # print('----')
                # print('--EMA--')
                # print(ema)
                # print('----')
                # print('--DM(+)--')
                # print(dp)
                # print('----')
                # print('--DM(-)--')
                # print(dm)
                # print('--ADX--')
                # print(adx)
                pos = (dp[-1] - dm[-1]) > 0 
                neg = (dp[-1] - dm[-1]) < 0 
                # print('----')
                # print("This is up: {}".format(pos))
                # print('----')
                # print("This is down: {}".format(neg))
                if pos == True: 
                    print("uptrend")
                    if adx > adx_high: 
                        print('a good market')
                        total = float(pos) * 100
                        print("Uptrending: % {:.3f}".format(total))
                        print("now we invest.Calculate price to buy")
                    if((ema[-1]) < closed_total[-1]):     
                        print("BUY!!!")
                        print("Bought: ${}".format(ema[-1]))
                        print("------")
                        print("sold at {}".format(closed_total[-1]))
                        
                        if (rsi_high > rsi[-1] > rsi_low) and (adx[-1] >20):
                            print("------")
                            print("BUY!!! MORE!!!!")                                
                            print("Bought: ${}".format(ema[-1]))
                            print("------")
                            print("sold at {}".format(closed_total[-1]))
                            profit += ema[-1] +closed_total[-1]                
                                
                    if neg == True:
                        if adx > adx_low:
                            print("short trade")  
                            print("-------------")  
                    else:
                        print('Current RSI: {:.2}\nCurrent ADX: {:.2}\nCurrent true EMA: ${}'.format(rsi[-1],adx[-1],ema[-1]))
                
                    # if dp[-1] < dm[-1]:
                    #     print("downtrend")   
                if neg == True:  
                    # print("----------------------")
                    print("downtrend")
                    count = 0
                    while count < 4:
                        
                        if final_value_tick[-2] > final_value_tick[-1]:
                            print("was lower")
                            count += 1
                            if count >= 4:
                                count == 0   
                                candle1 = float(open_price[-2]) + float(closed_price[-2])                                 
                                newCandle = float(open_price[-1]) + float(closed_price[-1])
                                if (candle1 < newCandle) and (rsi_high > rsi[-1] > rsi_low) and (adx[-1] >adx_high):  
                                    print("Uptrend")
                    else:  
                        print("Still downtrend")
                        print("Count: {}".format(count)) 
                    
                    # print("----------------------")
                    # print("count: {}".format(count))
                    if pos == True:
                        if (adx[-1] > adx_high):                            
                            print("look for buy signal")

                        while count < 4:
                            if final_value_tick[-2] > final_value_tick[-1]:
                                print("was lower")
                                count += 1
                        if count >= 4:
                            count == 0   
                            candle1 = float(open_price[-2]) + float(closed_price[-2])                                 
                            newCandle = float(open_price[-1]) + float(closed_price[-1])
                            if (candle1 < newCandle) and (rsi_high > rsi[-1] > rsi_low) and (adx[-1] >adx_high):  
                                print("Uptrend")
                        else:  
                            print("Still downtrend")
                            print("Count: {}".format(count)) 
                    else:   
                        print("blah market")
        # 
        # 
        print("----------------------") 
        print("updating....")
        
    
        
        
    # def ema(webS):
    #     day = 50
    webS = websocket.WebSocketApp(SOCKET,on_open=on_open,on_close=on_close, on_message=on_message)

    webS.run_forever()
    
bot("btc")
