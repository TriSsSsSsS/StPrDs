"""
Stock Data Downloader - Automated Script
Downloads stock data for Russell 1000 companies and saves to compressed CSV files
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import time
import logging
import warnings
import random

# Suppress yfinance warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', module='yfinance')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('download_log.txt'),
        logging.StreamHandler()
    ]
)

# Create data directory
DATA_DIR = Path("stock_data")
DATA_DIR.mkdir(exist_ok=True)

# Create earnings directory
EARNINGS_FILE = Path("earnings_dates.csv.gz")

# Russell 1000 Companies (as of August 22, 2025)
ALL_TICKERS = ["MMM","AOS","AAON","ABT","ABBV","ACHC","ACN","AYI","ADBE","ADT","WMS","AMD",
               "ACM","AES","AMG","AFRM","AFL","AGCO","A","ADC","AGNC","AL","APD","ABNB","AKAM",
               "ALK","ALB","ACI","AA","ARE","ALGN","ALLE","ALGM","LNT","ALSN","ALL","ALLY",
               "ALNY","GOOGL","GOOG","MO","AMZN","AMCR","DOX","AMTM","AS","AEE","AAL","AEP",
               "AXP","AFG","AMH","AIG","AMT","AWK","COLD","AMP","AME","AMGN","AMKR","APH","ADI",
               "AU","NLY","AM","AR","AON","APA","APG","APLS","APO","APPF","AAPL","AIT","AMAT",
               "APP","ATR","APTV","ARMK","ACGL","ADM","ARES","ANET","AWI","ARW","AJG","ASH",
               "AIZ","AGO","ALAB","ASTS","T","ATI","TEAM","ATO","AUR","ADSK","ADP","AN","AZO",
               "AVB","AVTR","AVY","CAR","AVT","AXTA","AXS","AXON","BKR","BALL","BAC","OZK",
               "BBWI","BAX","BDX","BRBR","BSY","BRK-B","BBY","BILL","BIO","TECH","BIIB","BMRN",
               "BIRK","BJ","BLK","BX","HRB","XYZ","OWL","BK","BA","BOKF","BKNG","BAH","BWA",
               "SAM","BSX","BYD","BFAM","BHF","BMY","BRX","AVGO","BR","BAM","BEPC","BRO","BF-A",
               "BF-B","BRKR","BC","BLDR","BG","BURL","BWXT","BXP","CHRW","CACI","CDNS","CZR",
               "CPT","CPB","COF","CAH","CAI","CSL","CG","KMX","CCL","CRS","CARR","CVNA","CAT",
               "CAVA","CBOE","CBRE","CDW","CE","CELH","COR","CNC","CNP","CERT","CF","CRL","SCHW",
               "CHTR","CHE","LNG","CVX","CHWY","CMG","CHH","CHRD","CB","CHD","CHDN","CIEN","CI",
               "CINF","CTAS","CRUS","CSCO","C","CFG","CIVI","CLVT","CLH","CWEN-A","CWEN","CLF",
               "CLX","NET","CME","CMS","CNA","CNH","KO","COKE","CGNX","CTSH","COHR","COIN","CL",
               "COLB","COLM","CMCSA","CMA","FIX","CBSH","CAG","CNXC","CFLT","COP","ED","STZ",
               "CEG","COO","CPRT","CORT","CNM","GLW","CPAY","CTVA","CSGP","COST","CTRA","COTY",
               "CPNG","CUZ","CR","CXT","CACC","CRH","CROX","CRWD","CCI","CCK","CSX","CUBE","CMI",
               "CW","CVS","DHI","DHR","DRI","DAR","DDOG","DVA","DAY","DECK","DE","DAL","DELL",
               "XRAY","DVN","DXCM","FANG","DKS","DLR","DDS","DOCU","DLB","DG","DLTR","D","DPZ",
               "DCI","DASH","DV","DOV","DOW","DOCS","DKNG","DBX","DTM","DTE","DUK","DUOL","DD",
               "BROS","DXC","DT","ELF","EXP","EWBC","EGP","EMN","ETN","EBAY","ECL","EIX","EW",
               "ELAN","ESTC","EA","ESI","ELV","EME","EMR","EHC","ENPH","ENTG","ETR","NVST","EOG",
               "EPAM","EPR","EQT","EFX","EQIX","EQH","ELS","EQR","ESAB","WTRG","ESS","EL","ETSY",
               "EEFT","EVR","EG","EVRG","ES","ECG","EXAS","EXEL","EXC","EXLS","EXE","EXPE","EXPD",
               "EXR","XOM","FFIV","FDS","FICO","FAST","FRT","FDX","FERG","FNF","FIS","FITB","FAF",
               "FCNCA","FHB","FHN","FR","FSLR","FE","FI","FIVE","FLEX","FND","FLO","FLS","FLUT",
               "FMC","FNB","F","FTNT","FTV","FBIN","FOXA","FOX","BEN","FRHC","FCX","FRPT","FYBR",
               "CFR","FTAI","FCN","GME","GLPI","GAP","GRMN","IT","GTES","GLIBA","GLIBK","GE",
               "GEHC","GEV","GEN","GNRC","GD","GIS","GM","G","GNTX","GPC","GILD","GTLB","GPN",
               "GFS","GLOB","GL","GMED","GDDY","GS","GGG","LOPE","GPK","GWRE","GXO","HAL","HALO",
               "HLNE","THG","HOG","HIG","HAS","HAYW","HCA","HR","DOC","HEI-A","HEI","JKHY","HSY",
               "HPE","HXL","DINO","HIW","HLT","HOLX","HD","HON","HRL","HST","HLI","HHH","HWM",
               "HPQ","HUBB","HUBS","HUM","HBAN","HII","HUN","H","IAC","IBM","IDA","IEX","IDXX",
               "ITW","ILMN","INCY","INFA","IR","INGM","INGR","INSM","INSP","PODD","INTC","IBKR",
               "ICE","IFF","IP","IPG","INTU","ISRG","IVZ","INVH","IONS","IPGP","IQV","IRDM",
               "IRM","ITT","JBL","J","JHX","JHG","JAZZ","JBHT","JEF","JNJ","JCI","JLL","JPM",
               "KRMN","KBR","K","KMPR","KVUE","KDP","KEY","KEYS","KRC","KMB","KIM","KMI","KNSL",
               "KEX","KKR","KLAC","KNX","KHC","KR","KD","LHX","LH","LRCX","LAMR","LW","LSTR",
               "LVS","LSCC","LAZ","LEA","LDOS","LEN","LEN-B","LII","DRS","LBRDA","LBRDK","LBTYA",
               "LBTYK","FWONA","FWONK","LLYVA","LLYVK","LNW","LLY","LECO","LNC","LIN","LINE",
               "LAD","LFUS","LYV","LKQ","LOAR","LMT","L","LPX","LOW","LPLA","LCID","LULU","LITE",
               "LYFT","LYB","MTB","MTSI","M","MSGS","MANH","MAN","CART","MPC","MKL","MKTX",
               "MAR","MMC","MLM","MRVL","MAS","MASI","MTZ","MA","MTDR","MTCH","MAT","MKC",
               "MCD","MCK","MDU","MPW","MEDP","MDT","MRK","META","MET","MTD","MTG","MGM",
               "MCHP","MU","MSFT","MSTR","MAA","MIDD","TIGO","MRP","MKSI","MRNA","MHK","MOH",
               "TAP","MDLZ","MDB","MPWR","MNST","MCO","MS","MORN","MOS","MSI","MP","MSA","MSM",
               "MSCI","MLI","MUSA","NDAQ","NTRA","NFG","NSA","NCNO","NTAP","NFLX","NBIX","NYT",
               "NWL","NEU","NEM","NWSA","NWS","NXST","NEE","NIQ","NKE","NI","NNN","NDSN","NSC",
               "NTRS","NOC","NCLH","NOV","NRG","NU","NUE","NTNX","NVT","NVDA","NVR","ORLY","OXY",
               "OGE","OKTA","ODFL","ORI","OLN","OLLI","OHI","OMC","ONON","ON","OMF","OKE","ONTO",
               "ORCL","OGN","OSK","OTIS","OVV","OC","PCAR","PKG","PLTR","PANW","PK","PH","PSN",
               "PAYX","PAYC","PCTY","PYPL","PEGA","PENN","PAG","PNR","PEN","PEP","PFGC","PR",
               "PRGO","PFE","PCG","PM","PSX","PPC","PNFP","PNW","PINS","PLNT","PNC","POOL",
               "BPOP","POST","PPG","PPL","TROW","PRI","PRMB","PFG","PCOR","PG","PGR","PLD",
               "PB","PRU","PTC","PSA","PEG","PHM","PSTG","PVH","QGEN","QRVO","QCOM","PWR","QS",
               "DGX","QXO","RAL","RL","RRC","RJF","RYN","RBA","RBC","O","RDDT","RRX","REG",
               "REGN","RF","RGA","RS","RNR","RGEN","RSG","RMD","QSR","RVMD","RVTY","REXR",
               "REYN","RH","RNG","RITM","RIVN","RLI","RHI","HOOD","RBLX","RKT","RKLB","ROK",
               "ROIV","ROKU","ROL","ROP","ROST","RCL","RGLD","RPRX","RPM","RTX","RBRK","RYAN",
               "R","SPGI","SAIA","SAIL","SAIC","CRM","SLM","IOT","SNDK","SRPT","SBAC","HSIC",
               "SLB","SNDR","SMG","SEB","SEE","SEIC","SRE","ST","S","SCI","NOW","SN","SHW",
               "FOUR","SLGN","SPG","SSD","SIRI","SITE","SWKS","SFD","SJM","SW","SNA","SNOW",
               "SOFI","SOLS","SOLV","SGI","SON","SHC","SO","SCCO","SSB","LUV","SPR","SPOT",
               "SFM","SSNC","STAG","SARO","SWK","SBUX","STWD","STT","STLD","STE","SF","SYK",
               "SMMT","SUI","SMCI","SYF","SNPS","SNV","SYY","TMUS","TTWO","TLN","TPR","TRGP",
               "TGT","SNX","FTI","TDY","TFX","TEM","THC","TDC","TER","TSLA","TTEK","TXN","TPL",
               "TXRH","TXT","TMO","TFSL","THO","TKR","TJX","TKO","TOST","TOL","BLD","TTC",
               "TPG","TSCO","TTD","TW","TT","TDG","TRU","TNL","TRV","TREX","TRMB","TFC",
               "DJT","TWLO","TYL","TSN","UHAL","UHAL-B","USB","UBER","UI","UDR","UGI","PATH",
               "ULTA","RARE","UAA","UA","UNP","UAL","UPS","URI","UTHR","UWMC","UNH","U","OLED",
               "UHS","UNM","USFD","MTN","VLO","VMI","VVV","VEEV","VTR","VLTO","VRSN","VRSK",
               "VZ","VRTX","VRT","VFC","VTRS","VICI","VIK","VKTX","VNOM","VIRT","V","VST",
               "VNT","VNO","VOYA","VMC","WPC","WRB","GWW","WAB","WMT","DIS","WBD","WM","WAT",
               "WSO","W","WFRD","WBS","WEC","WFC","WELL","WEN","WCC","WST","WAL","WDC","WU",
               "WLK","WEX","WY","WHR","WTM","WMB","WSM","WTW","WSC","WING","WTFC","WWD","WDAY",
               "WH","WYNN","XEL","XP","XPO","XYL","YETI","YUM","ZBRA","ZG","Z","ZBH","ZION",
               "ZTS","ZM","GTM","ZS"]


def download_ticker_data(ticker, start_date, end_date, interval="30m"):
    """
    Download stock data for a single ticker
    Returns DataFrame with only required columns
    """
    try:
        # Download data from Yahoo Finance
        df = yf.download(
            ticker, 
            start=start_date, 
            end=end_date, 
            interval=interval,
            progress=False
        )
        
        if df.empty:
            logging.warning(f"No data available for {ticker}")
            return None
        
        # Flatten MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        # Reset index to make Datetime a column
        df = df.reset_index()
        
        # Add ticker column
        df['Ticker'] = ticker
        
        # Select only required columns
        required_columns = ['Datetime', 'Close', 'High', 'Low', 'Open', 'Volume', 'Ticker']
        df = df[required_columns]
        
        return df
        
    except Exception as e:
        logging.error(f"Error downloading {ticker}: {str(e)}")
        return None


def save_data(ticker, df):
    """
    Save data to compressed CSV file (append mode)
    """
    file_path = DATA_DIR / f"{ticker}.csv.gz"
    
    try:
        # If file exists, load and append new data
        if file_path.exists():
            existing_df = pd.read_csv(file_path, compression='gzip', parse_dates=['Datetime'])
            df = pd.concat([existing_df, df], ignore_index=True)
            # Remove duplicates based on Datetime and Ticker
            df = df.drop_duplicates(subset=['Datetime', 'Ticker'], keep='last')
        
        # Sort by Datetime
        df = df.sort_values('Datetime')
        
        # Save to compressed CSV
        df.to_csv(file_path, compression='gzip', index=False)
        
        return True
    except Exception as e:
        logging.error(f"Error saving data for {ticker}: {str(e)}")
        return False


def get_earnings_dates(ticker):
    """
    Get earnings dates for a ticker
    Returns DataFrame with Ticker and Earnings_Date columns
    """
    try:
        stock = yf.Ticker(ticker)
        earnings_dates = stock.earnings_dates
        
        if earnings_dates is None or earnings_dates.empty:
            return None
        
        # Reset index to get dates as a column
        df = earnings_dates.reset_index()
        df = df.rename(columns={'index': 'Earnings_Date'})
        
        # Add ticker column
        df['Ticker'] = ticker
        
        # Select only date and ticker
        df = df[['Ticker', 'Earnings_Date']]
        
        return df
        
    except Exception as e:
        logging.error(f"Error getting earnings for {ticker}: {str(e)}")
        return None


def save_earnings_data(all_earnings_df):
    """
    Save all earnings data to a single compressed CSV file
    """
    try:
        # If file exists, load and append new data
        if EARNINGS_FILE.exists():
            existing_df = pd.read_csv(EARNINGS_FILE, compression='gzip', parse_dates=['Earnings_Date'])
            all_earnings_df = pd.concat([existing_df, all_earnings_df], ignore_index=True)
            # Remove duplicates
            all_earnings_df = all_earnings_df.drop_duplicates(subset=['Ticker', 'Earnings_Date'], keep='last')
        
        # Sort by Ticker and Date
        all_earnings_df = all_earnings_df.sort_values(['Ticker', 'Earnings_Date'])
        
        # Save to compressed CSV
        all_earnings_df.to_csv(EARNINGS_FILE, compression='gzip', index=False)
        
        logging.info(f"📊 Saved earnings data: {len(all_earnings_df)} records")
        return True
        
    except Exception as e:
        logging.error(f"Error saving earnings data: {str(e)}")
        return False


def save_data(ticker, df):
    """
    Save data to compressed CSV file (append mode)
    """
    file_path = DATA_DIR / f"{ticker}.csv.gz"
    
    try:
        # If file exists, load and append new data
        if file_path.exists():
            existing_df = pd.read_csv(file_path, compression='gzip', parse_dates=['Datetime'])
            df = pd.concat([existing_df, df], ignore_index=True)
            # Remove duplicates based on Datetime and Ticker
            df = df.drop_duplicates(subset=['Datetime', 'Ticker'], keep='last')
        
        # Sort by Datetime
        df = df.sort_values('Datetime')
        
        # Save to compressed CSV
        df.to_csv(file_path, compression='gzip', index=False)
        
        return True
    except Exception as e:
        logging.error(f"Error saving data for {ticker}: {str(e)}")
        return False


def download_all(tickers, start_date, end_date, interval="30m", delay=0.2):
    """
    Download data for all tickers with progress tracking
    Also collects earnings dates for all tickers
    """
    total = len(tickers)
    successful = 0
    failed = 0
    failed_tickers = []
    all_earnings = []
    
    logging.info(f"Starting download of {total} tickers...")
    logging.info(f"Period: {start_date} to {end_date}")
    logging.info(f"Interval: {interval}")
    
    for i, ticker in enumerate(tickers, 1):
        logging.info(f"[{i}/{total}] Processing {ticker}...")
        
        # Download price data
        df = download_ticker_data(ticker, start_date, end_date, interval)
        
        if df is not None and not df.empty:
            if save_data(ticker, df):
                successful += 1
                logging.info(f"✅ {ticker}: {len(df)} records saved")
            else:
                failed += 1
                failed_tickers.append(ticker)
        else:
            failed += 1
            failed_tickers.append(ticker)
            logging.error(f"❌ {ticker}: Failed to download")
        
        # Get earnings dates (less verbose)
        earnings_df = get_earnings_dates(ticker)
        if earnings_df is not None and not earnings_df.empty:
            all_earnings.append(earnings_df)
        
        # Rate limiting
        time.sleep(delay)
    
    # Save all earnings data
    if all_earnings:
        combined_earnings = pd.concat(all_earnings, ignore_index=True)
        save_earnings_data(combined_earnings)
    
    logging.info("=" * 50)
    logging.info("Download complete!")
    logging.info(f"Successful: {successful}/{total}")
    logging.info(f"Failed: {failed}/{total}")
    logging.info("=" * 50)
    
    return successful, failed, failed_tickers
    
    logging.info("=" * 50)
    logging.info("Download complete!")
    logging.info(f"Successful: {successful}/{total}")
    logging.info(f"Failed: {failed}/{total}")
    logging.info("=" * 50)
    
    return successful, failed, failed_tickers


def create_sample_file():
    """
    Create a readable sample file with a random ticker's data
    Shows first 3 days and last 30 days of data
    """
    try:
        # Get all existing CSV files
        csv_files = list(DATA_DIR.glob("*.csv.gz"))
        
        if not csv_files:
            logging.warning("No CSV files found to create sample")
            return
        
        # Select a random file
        random_file = random.choice(csv_files)
        ticker = random_file.stem.replace('.csv', '')
        
        # Read the data
        df = pd.read_csv(random_file, compression='gzip', parse_dates=['Datetime'])
        
        if df.empty:
            logging.warning(f"Empty data for {ticker}")
            return
        
        # Sort by datetime
        df = df.sort_values('Datetime')
        
        # Get first 3 days and last 30 days
        first_3_days = df.head(3 * 13)  # 3 days * ~13 records per day (30min intervals)
        last_30_days = df.tail(30 * 13)  # 30 days * ~13 records per day
        
        # Create sample file
        sample_path = Path('sample_data.txt')
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(sample_path, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write(f"STOCK DATA SAMPLE - {ticker}\n")
            f.write(f"Generated: {current_date}\n")
            f.write(f"Total records in file: {len(df)}\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("FIRST 3 DAYS OF DATA:\n")
            f.write("-" * 80 + "\n")
            f.write(first_3_days.to_string(index=False))
            f.write("\n\n")
            
            f.write("LAST 30 DAYS OF DATA:\n")
            f.write("-" * 80 + "\n")
            f.write(last_30_days.to_string(index=False))
            f.write("\n\n")
            f.write("=" * 80 + "\n")
            f.write(f"End of sample for {ticker}\n")
            f.write("=" * 80 + "\n")
        
        logging.info(f"📄 Sample file created with data from {ticker}")
        logging.info(f"   First 3 days: {len(first_3_days)} records")
        logging.info(f"   Last 30 days: {len(last_30_days)} records")
        
    except Exception as e:
        logging.error(f"Error creating sample file: {str(e)}")


def main():
    """Main execution function"""
    # Calculate dates (from 1 day ago to today)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)
    
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    
    logging.info(f"📅 Download period: {start_str} to {end_str}")
    logging.info(f"📆 Days included: 2 days (from 1 day ago to today)")
    logging.info(f"⏰ Interval: 1 minute")
    logging.info(f"📊 Total tickers: {len(ALL_TICKERS)}")
    
    # Run download
    start_time = time.time()
    successful, failed, failed_tickers = download_all(
        tickers=ALL_TICKERS,
        start_date=start_str,
        end_date=end_str,
        interval="1m",
        delay=0.2
    )
    
    elapsed_time = time.time() - start_time
    
    # Append simplified summary to log
    log_path = Path('download_log.txt')
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_path, 'a') as f:
        if failed == 0:
            f.write(f"{successful}/{len(ALL_TICKERS)} - {current_date}\n")
        else:
            f.write(f"{successful}/{len(ALL_TICKERS)} - Failed: {failed_tickers} - {current_date}\n")
    
    logging.info(f"⏱️  Total time: {elapsed_time/60:.2f} minutes")
    logging.info(f"✅ Successfully downloaded: {successful}/{len(ALL_TICKERS)} tickers")
    logging.info(f"❌ Failed: {failed}/{len(ALL_TICKERS)} tickers")
    
    # Count files
    csv_files = list(DATA_DIR.glob("*.csv.gz"))
    logging.info(f"📁 Total files in directory: {len(csv_files)}")
    
    # Create sample file with random ticker data
    create_sample_file()


if __name__ == "__main__":
    main()
