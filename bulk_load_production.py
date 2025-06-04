import requests
import time
from datetime import datetime

BASE_URL = "https://django-esg-150929446067.europe-west1.run.app"


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

def get_csrf_token(session, url):

    try:
        response = session.get(url)
        if 'csrfmiddlewaretoken' in response.text:
            start = response.text.find('name="csrfmiddlewaretoken" value="') + 34
            end = response.text.find('"', start)
            return response.text[start:end]
    except:
        pass
    return None

def load_ticker_to_production(ticker, start_date='2025-04-01', end_date='2025-06-01'):

    
    url = f"{BASE_URL}/upload/stocks/"
    session = requests.Session()
    
    try:

        csrf_token = get_csrf_token(session, url)
        
        data = {
            'ticker': ticker,
            'date_from': start_date,
            'date_to': end_date,
        }
        
        if csrf_token:
            data['csrfmiddlewaretoken'] = csrf_token
        

        response = session.post(url, data=data, timeout=30)
        
        if response.status_code == 200:
            if 'success' in response.text.lower() or 'loaded successfully' in response.text:
                return True, "Success"
            elif 'error' in response.text.lower():
    
                error_start = response.text.find('error')
                error_text = response.text[error_start:error_start+100]
                return False, error_text[:50]
            else:
                return False, "Unknown response"
        else:
            return False, f"HTTP {response.status_code}"
            
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)[:50]

def bulk_load_all_tickers():

    
    start_date = '2025-04-01'
    end_date = '2025-06-01'

    
    success_count = 0
    failed_tickers = []
    
    for i, ticker in enumerate(TICKERS, 1):
        print(f"[{i:2d}/{len(TICKERS)}] {ticker:12s} ... ", end="", flush=True)
        
        success, message = load_ticker_to_production(ticker, start_date, end_date)
        
        if success:
            print("✅ OK")
            success_count += 1
        else:
            print(f"❌ {message}")
            failed_tickers.append((ticker, message))

        time.sleep(1)

        if i % 10 == 0:
            print(f"   🔄 Пауза... ({success_count}/{i} успешных)")
            time.sleep(3)

    

if __name__ == "__main__":
    start_time = datetime.now()

    bulk_load_all_tickers()
        

