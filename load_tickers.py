import os
import sys
import django

# Настройка Django
sys.path.append('/home/daniil/Projects/oleg/django_esg/project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from stocks_app.services.stock_service import run
from datetime import datetime, timedelta

# Список тикеров
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

def load_historical_data(start_date='2024-01-01', end_date='2024-12-31'):
    """Загрузка исторических данных для всех тикеров"""
    
    print(f"🚀 Начинаем загрузку данных для {len(TICKERS)} тикеров")
    print(f"📅 Период: {start_date} - {end_date}")
    print("-" * 50)
    
    success_count = 0
    failed_tickers = []
    
    for i, ticker in enumerate(TICKERS, 1):
        print(f"[{i}/{len(TICKERS)}] Загружаем {ticker}...", end=" ")
        
        try:
            run(ticker, start_date, end_date)
            print("✅ OK")
            success_count += 1
        except Exception as e:
            print(f"❌ Ошибка: {str(e)[:50]}...")
            failed_tickers.append(ticker)
    
    print("\n" + "=" * 50)
    print(f"✅ Успешно загружено: {success_count} тикеров")
    print(f"❌ Ошибок: {len(failed_tickers)} тикеров")
    
    if failed_tickers:
        print(f"Проблемные тикеры: {', '.join(failed_tickers)}")

if __name__ == "__main__":
    # Загрузка данных за 2024 год
    load_historical_data('2024-05-01', '2025-05-31')
