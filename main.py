import pandas as pd
import numpy as nm
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
yf.pdr_override()

def main():
    
    stock=input("Enter a stock ticker symbol: ")
    print(stock)
    
    startyear=2018
    startmonth=1
    startday=1
    start=dt.datetime(startyear, startmonth, startday)
    now=dt.datetime.now()
    
    hist = pdr.get_data_yahoo(stock, start, now)
    tick = yf.Ticker(stock)
    
    period=60
    pmin="minimum_"+str(period)+"_day"
    hist[pmin]=hist.iloc[:,4].rolling(window=period).min()
    pmax="maximum_"+str(period)+"_day"
    hist[pmax]=hist.iloc[:,4].rolling(window=period).max()
    
    var = 0.02
    pos = 0
    trade = 0
    pl = 0
    percentchange=[]

    for i in hist.index:
        close=hist["Adj Close"][i]
        if(close<=(hist[pmin][i]+(hist[pmin][i]*var)) and ((hist[pmax][i]-hist[pmin][i])/hist[pmin][i])> 0.5):
            if(pos==0):
                buyprice=close
                pos=1
                print(str(i)+" buy at "+str(buyprice) + " min " +str(hist[pmin][i]) + " max " +str(hist[pmax][i])  )
                
        elif (pos==1):
            if(close <= (buyprice-(buyprice*0.1))):
                sellprice=close
                pos=0
                print(str(i)+" sell at "+str(close)+" hit stoploss"+ " min " +str(hist[pmin][i]))
                pc=(sellprice/buyprice-1)*100
                percentchange.append(pc)

                         
            elif(close>=(hist[pmax][i]-(hist[pmax][i]*var))):
                sellprice=close
                pos=0
                print(str(i)+" sell at "+str(close)+ " max " +str(hist[pmax][i]))
                pc=(sellprice/buyprice-1)*100
                percentchange.append(pc)

    print(percentchange)

    gains=0
    nrgains=0
    losses=0
    nrlosses=0
    totalreturn=1

    for i in percentchange:
        if(i>0):
            gains+=i
            nrgains+=1
        else:
            losses=i
            nrlosses+=1
        totalreturn=totalreturn*((i/100)+1)
        
    totalreturn=round((totalreturn-1)*100,2)

    if(nrgains>0):
        avgGain=gains/nrgains
        maxR=str(max(percentchange))
    else:
        avgGain=0
        maxR="undefined"
        
    if(nrlosses>0):
        avgLoss=losses/nrlosses
        maxL=str(min(percentchange))
    else:
        avgLoss=0
        maxL="undefined"

    if (avgLoss!=0):
        ratio=str(-avgGain/avgLoss)
    else:
        ratio="inf"
        
    if(nrgains>0 or nrlosses>0):
        battingAvg=nrgains/(nrgains+nrlosses)
    else:
        battingAvg=0
        
    print()
    print("Results for " + stock + " going back to " + str(hist.index[0]) + ", Sample size: " + str(nrgains + nrlosses) + " trades")
    print("Batting Avg: "+ str(battingAvg))
    print("Gain/Loss ratio: " + ratio)
    print("Average gain: " + str(avgGain))
    print("Average loss: " + str(avgLoss))
    print("Max return: " + str(maxR))
    print("Max loss: " + str(maxL))
    print("Total return over " + str(nrgains+nrlosses) + " trades: " + str(totalreturn) + "%")

       
if __name__ == '__main__':
    main()
