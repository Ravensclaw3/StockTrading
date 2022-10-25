import pandas as pd
import numpy as nm
import yfinance as yf
import datetime as dt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pandas_datareader import data as pdr
yf.pdr_override()
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('c://python/client_secret.json', scope)
client = gspread.authorize(credentials)

def strategy(stock, startyear=2022, startmonth=1, startday=1, period=60, var = 0.02):
    start = dt.datetime(startyear, startmonth, startday)
    now = dt.datetime.now()

    data = pdr.get_data_yahoo(stock, start, now)

    pmin="minimum_"+str(period)+"_day"
    data[pmin]=data.iloc[:,4].rolling(window=period).min()
    pmax="maximum_"+str(period)+"_day"
    data[pmax]=data.iloc[:,4].rolling(window=period).max()

    pos = 0
    action = ""
    trade = 0
    pl = 0
    percentchange = []

    for i in data.index:
        close=data["Adj Close"][i]
        if(close<=(data[pmin][i]+(data[pmin][i]*var))):
            if(pos==0):
                buyprice=close
                pos=1
                action = "Buy"
            else:
                action = "Wait for sell"
                
        elif (pos==1):
            if(close <= (buyprice-(buyprice*0.1))):
                pos=0
                action = "Stoploss Sell"
                                         
            elif(close>=(data[pmax][i]-(data[pmax][i]*var))):
                pos=0
                action = "Sell"
        else:
            action = "Wait for buy"
                
    result = {}
    result["Stock"] = stock
    result["Action"] = action

    return result

def main():

    tickers = ["AAL","AAON","AAPL","ABBV","ABNB","ABT","ACEV","ACM","ACN","ADBE","ADI","ADM","ADP","ADSK","AEM","AER","AFRM","AGNC","AI","AIG","AKAM","ALB","ALGN","ALL","ALNY","AM","AMAT","AMBA","AMD","AME","AMGN","AMRS","AMT","AMZN","APD","API","APP","APPH","APPN","APPS","AR","ARCH","ARVL","ASAN","ASML","ATER","ATVI","AVAV","AVGO","AVLR","AWK","AXP","AYX","AZN","BA","BABA","BAC","BAM","BAMR","BAND","BBBY","BCS","BDTX","BEAM","BG","BHC","BHF","BHP","BIDU","BIIB","BILI","BILL","BK","BKNG","BLK","BLNK","BMBL","BMRN","BMY","BNGO","BNTX","BOC","BOX","BP","BRK-B","BRKR","BSX","BTAI","BTCM","BTG","BTU","BYD","BYND","BZUN","C","CAG","CARA","CARR","CAT","CCJ","CCL","CCXI","CDNS","CEG","CELH","CEQP","CEVA","CFLT","CGC","CHKP","CHPT","CHTR","CI","CL","CLF","CLNE","CLOV","CLPT","CMA","CMCSA","CME","CMG","CMPS","CNQ","COE","COF","COHR","COIN","COP","COST","COUR","CPB","CPNG","CRCT","CRM","CRNC","CRON","CROX","CRSP","CRSR","CRUS","CRWD","CSCO","CSIQ","CSX","CTAS","CTRM","CTSH","CTVA","CURI","CVE","CVET","CVI","CVNA","CVS","CVX","CWH","CXW","CYBR","DAL","DAO","DASH","DB","DBX","DDD","DDOG","DE","DELL","DEO","DHI","DHR","DINO","DIS","DISH","DJCO","DK","DKNG","DLR","DLTR","DM","DMTK","DNA","DNMR","DNN","DNOW","DOCN","DOCU","DOW","DQ","DUK","DVN","DXCM","DD","EA","EBAY","ECPG","EDIT","EDR","EDU","EGLE","EGO","EL","EMR","ENPH","ENTG","EPD","EPR","EQIX","EQNR","EQT","ERIC","ESTC","ET","ETRN","ETSY","EXAS","EXC","EXPE","F","FARO","FAST","FCEL","FCX","FDX","FISV","FIVN","FLGT","FMC","FNV","FOX","FOXA","FSLR","FSLY","FSR","FTCH","FTV","FUBO","FUTU","FVRR","GAIN","GD","GDRX","GE","GEO","GEVO","GILD","GIS","GLW","GM","GNUS","GOLD","GOOG","GOOGL","GPN","GPRO","GRBK","GRMN","GRVY","GRWG","GS","GSK","GXO","HAL","HAS","HCM","HD","HDB","HEAR","HIFS","HIMX","HLN","HMC","HNST","HOG","HOLX","HON","HOOD","HPE","HSIC","HUBS","HUYA","HZNP","IBM","IBRX","ICE","ICL","IDXX","IFF","IHS","IIPR","IIVI","ILMN","IMO","INCY","INMD","INO","INSG","INTC","INTU","INTZ","IQ","IQV","IRBT","IREN","IRM","ISRG","ITW","IVR","JAZZ","JBHT","JD","JMIA","JNJ","JOBY","JPM","K","KARO","KD","KDP","KEYS","KGC","KHC","KLAC","KMI","KNSL","KO","KODK","KR","KTOS","LAC","LAND","LAZR","LBRDK","LBTYA","LBTYK","LCID","LDOS","LEU","LI","LILM","LIN","LLY","LMND","LMT","LNG","LOB","LOGI","LOPE","LOW","LPSN","LRCX","LRN","LTHM","LULU","LUMN","LUV","LYV","MA","MAIN","MANU","MAR","MARA","MASI","MAT","MAXR","MBUU","MCD","MCHP","MCO","MDB","MDLZ","MDT","MELI","MET","META","MGNI","MHK","MKL","MMM","MMP","MNMD","MNST","MO","MODG","MOS","MP","MPLX","MRK","MRNA","MRVL","MS","MSFT","MSTR","MT","MTCH","MTTR","MU","MVIS","MVST","NCLH","NCNO","NDAQ","NEE","NEM","NET","NEWR","NFLX","NIO","NKE","NKLA","NLOK","NLY","NMG","NNDM","NOC","NOK","NOW","NTES","NTGR","NTLA","NTNX","NUE","NVAX","NVCR","NVDA","NVO","NVS","NVTA","NXE","NXPI","NYT","O","OGN","OHI","OKTA","OM","OMER","ON","ONL","OPEN","ORCL","ORLY","OSTK","OTIS","OXY","OZON","PAAS","PACB","PANW","PARA","PATH","PAYC","PAYX","PBI","PCAR","PDD","PEGA","PENN","PEP","PETS","PFE","PG","PGNY","PING","PINS","PKI","PL","PLTR","PLUG","PM","PPL","PRLB","PRPL","PTON","PUBM","PYPL","QCOM","QDEL","QRTEA","QRVO","QS","QSI","QTRX","QURE","RACE","RBLX","RCL","RDFN","REGN","RH","RHP","RIO","RIOT","RIVN","RKLB","RKT","RNG","ROKU","ROP","ROST","RRC","RSG","RTX","RUN","SAFE","SAGE","SAM","SAVA","SBAC","SBLK","SBNY","SBSW","SBUX","SCCO","SCPL","SDGR","SE","SEDG","SFIX","SGEN","SGHC","SH","SHEL","SHOP","SHW","SIRI","SIVB","SKLZ","SKY","SLB","SLDP","SMAR","SNAP","SNDL","SNOW","SNPS","SNY","SO","SOFI","SONO","SONY","SOS","SPCE","SPG","SPGI","SPLK","SPOT","SPR","SPT","SPWR","SQ","SQM","SQSP","SRAD","SRG","SSTK","SSYS","STAG","STEM","STLA","STM","STNE","STX","SU","SUPN","SWK","SWKS","SWN","SYF","SYK","T","TAK","TAP","TCOM","TDG","TDOC","TEAM","TECK","TELL","TENB","TGT","THO","TIGR","TLRY","TLS","TM","TMDX","TME","TMO","TMUS","TPIC","TREX","TRIP","TRMB","TROW","TRV","TRVG","TSCO","TSLA","TSM","TTC","TTCF","TTD","TTWO","TWLO","TWOU","TWTR","TXG","TXN","U","UAA","UBA","UBER","UCTT","UEC","UI","UL","ULTA","UMC","UNH","UNP","UPS","UPST","USB","UUUU","V","VALE","VCEL","VEEV","VIPS","VIXY","VMW","VNET","VNT","VOD","VRSK","VRTX","VTRS","VUZI","VZ","WAB","WB","WBA","WBD","WD","WDAY","WDC","WDS","WFC","WISH","WIX","WKHS","WM","WMB","WMG","WMT","WNS","WOLF","WPM","WRAP","WWE","WYNN","X","XNCR","XOM","XPEV","XPO","XRAY","YETI","YUM","Z","ZBH","ZBRA","ZEN","ZIMV","ZM","ZS","ZTS"]
   # tickers = ["AAL","AAON"]
    for i, ticker in enumerate(tickers):
        if i == 0:
            tickersReturn = pd.DataFrame(data=strategy(stock = ticker, startyear=2022, startmonth=1, startday=1, period=60, var = 0.02), index=[i])
        else:
            tickersReturn = pd.concat([tickersReturn,pd.DataFrame(data=strategy(stock = ticker, startyear=2022, startmonth=1, startday=1, period=60, var = 0.02), index=[i])])

    tickersReturn.to_csv(f'actionForToday.csv')



    spreadsheet = client.open('DailyTradeAction')

    with open('actionForToday.csv', 'r') as file_obj:
        content = file_obj.read()
        client.import_csv(spreadsheet.id, data=content)

    return 0

if __name__ == '__main__':
    main()
