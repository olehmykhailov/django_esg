import requests
import time

BASE_URL = "https://django-esg-150929446067.europe-west1.run.app"
TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA']

def load_ticker_via_web(ticker):

    
    url = f"{BASE_URL}/upload/stocks/"
    
    data = {
        'ticker': ticker,
        'date_from': '2024-05-01',
        'date_to': '2025-05-31'
    }
    
    try:
        session = requests.Session()
        response = session.get(url)
        
        if 'csrfmiddlewaretoken' in response.text:
            csrf_start = response.text.find('csrfmiddlewaretoken') + len('csrfmiddlewaretoken') + 9
            csrf_end = response.text.find('"', csrf_start)
            csrf_token = response.text[csrf_start:csrf_end]
            data['csrfmiddlewaretoken'] = csrf_token
        

        response = session.post(url, data=data)
 
            
    except Exception as e:
        return False

if __name__ == "__main__":

    
    for ticker in TICKERS:
        load_ticker_via_web(ticker)
        time.sleep(2) 
    

