import os
import sys
import django
import time
from datetime import datetime


sys.path.append('/home/daniil/Projects/oleg/django_esg/project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from stocks_app.services.stock_service import run


TICKERS = [
    'AAPL', '005930.KS', 'SONY', 'DELL', 'HPQ', '0992.HK', '2357.TW', '2353.TW', 
    'MSFT', 'GOOGL', 'INTC', 'AMD', 'NVDA', 'QCOM', 'AVGO', 'TXN', 'MU', 
    '000660.KQ', 'TSM', 'ASML', 'LOGI', 'CRSR', 'WDC', 'STX', 'NTAP', 'ANET', 
    'SMCI', 'PSTG', 'CAN', 'DDD', '6752.T', '066570.KQ', '6702.T', '6701.T', 
    '6501.T', '6503.T', '6971.T', 'SIE.DE', 'SU.PA', 'ETN', 'ROK', 'HON', 
    'EMR', 'GE', 'PHIA.AS', 'TDY', 'IBM', 'ARM', 'NXPI', 'ADI', 'IFX.DE', 
    'STM', 'ON', 'MRVL', 'MCHP', 'SWKS', 'ZBRA', 'GRMN', 'GPRO', 'TRMB', 
    'HEXA-B.ST', 'AMBA', 'MPWR', 'LRCX', 'KLAC', 'TER', 'COHR', 'MTSI', 
    'DIOD', 'SYNA', 'NVMI', 'UMC', 'HIMX', 'AEHR', 'ACLS', 'CAMT', 'SMTC', 
    'FORM', 'ICHR', 'LSCC', 'LITE', 'IPGP', 'MKSI', 'VSH', 'VECO', 'CRUS', 
    'POWI', 'WOLF', 'QRVO', 'OLED', 'FLEX', 'BHE', 'SANM', 'FN'
]

def load_all_real_data():

    start_date = '2024-04-01'
    end_date ='2025-06-31'
    
    
    success_count = 0
    failed_tickers = []
    
    for i, ticker in enumerate(TICKERS, 1):
        print(f"[{i:2d}/{len(TICKERS)}] {ticker:12s} ... ", end="", flush=True)
        
        try:
            run(ticker, start_date, end_date)
            success_count += 1

            time.sleep(0.5)
            
        except Exception as e:
            error_msg = str(e)[:40] + "..." if len(str(e)) > 40 else str(e)
            print(f"❌ Ошибка: {error_msg}")
            failed_tickers.append(ticker)
    
    
    if failed_tickers:
        for ticker in failed_tickers:
            print(f"  - {ticker}")

        print(f"FAILED_TICKERS = {failed_tickers}")

if __name__ == "__main__":
    start_time = datetime.now()
    
    load_all_real_data()
    
    end_time = datetime.now()
    duration = end_time - start_time
