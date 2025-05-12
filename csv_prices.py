import yfinance as yf
import pandas as pd
import datetime
import time

# Исходные данные о компаниях
companies_raw_data = """
Ticker,Company
AAPL,Apple Inc
005930.KS,Samsung Electronics
SONY,Sony Group Corporation
DELL,Dell Technologies
HPQ,HP Inc
0992.HK,Lenovo Group
2357.TW,Quanta Computer
2353.TW,Pegatron Corporation
MSFT,Microsoft Corporation
GOOGL,Alphabet Inc Google
INTC,Intel Corporation
AMD,Advanced Micro Devices Inc
NVDA,NVIDIA Corporation
QCOM,Qualcomm Incorporated
AVGO,Broadcom Inc
TXN,Texas Instruments
MU,Micron Technology Inc
000660.KQ,SK hynix
TSM,Taiwan Semiconductor Manufacturing Company TSMC
ASML,ASML Holding
LOGI,Logitech International SA
CRSR,Corsair Gaming Inc
WDC,Western Digital Corporation
STX,Seagate Technology
NTAP,NetApp Inc
ANET,Arista Networks Inc
SMCI,Super Micro Computer Inc
PSTG,Pure Storage Inc
CAN,Canaan Inc
DDD,D Systems Corporation
CAJ,Canon Inc
6752.T,Panasonic Corporation
066570.KQ,LG Electronics
6502.T,Toshiba Corporation
6702.T,Fujitsu Limited
6701.T,NEC Corporation
6501.T,Hitachi Ltd
6503.T,Mitsubishi Electric Corporation
6971.T,Kyocera Corporation
SIE.DE,Siemens AG
ABB,ABB Ltd
SU.PA,Schneider Electric
ETN,Eaton Corporation
ROK,Rockwell Automation Inc
HON,Honeywell International Inc
EMR,Emerson Electric Co
GE,General Electric Company
PHIA.AS,Koninklijke Philips NV
TDY,Teledyne Technologies Incorporated
IBM,International Business Machines Corporation
ARM,Arm Holdings
NXPI,NXP Semiconductors
ADI,Analog Devices Inc
IFX.DE,Infineon Technologies AG
STM,STMicroelectronics
ON,ON Semiconductor Corporation
MRVL,Marvell Technology Inc
MCHP,Microchip Technology Incorporated
SWKS,Skyworks Solutions Inc
ZBRA,Zebra Technologies Corporation
GRMN,Garmin Ltd
GPRO,GoPro Inc
TRMB,Thermo Fisher Scientific
HEXA-B.ST,Hexagon AB
AMBA,Ambarella Inc
MPWR,Monolithic Power Systems Inc
LRCX,Lam Research Corporation
KLAC,KLA Corporation
TER,Teradyne Inc
COHR,Coherent Inc
MTSI,MACOM Technology Solutions Holdings Inc
DIOD,Diodes Incorporated
SYNA,Synaptics Incorporated
NVMI,Nova Measuring Instruments Ltd
UMC,United Microelectronics Corporation
HIMX,Himax Technologies Inc
AEHR,AEHR Test Systems
ACLS,Axcelis Technologies Inc
CAMT,Camtek Ltd
SMTC,Semtech Corporation
FORM,FormFactor Inc
ICHR,Ichor Systems Inc
LSCC,Lattice Semiconductor Corporation
LITE,Lumentum Holdings Inc
IPGP,IPG Photonics Corporation
MKSI,MKS Instruments Inc
VSH,Vishay Intertechnology Inc
VECO,Veeco Instruments Inc
CRUS,Cirrus Logic Inc
POWI,Power Integrations Inc
WOLF,Wolfspeed Inc
QRVO,Qorvo Inc
OLED,Universal Display Corporation
FLEX,Flex Ltd
BHE,Benchmark Electronics Inc
SANM,Sanmina Corporation
FN,Fabrinet
"""

# Создаем словарь Ticker: CompanyName и отдельный список тикеров для итерации
# Это позволит сохранить порядок и избежать дубликатов тикеров,
# но при этом иметь быстрый доступ к названию компании по тикеру.
ticker_to_company_map = {}
ordered_tickers = []

for line in companies_raw_data.strip().split('\n'):
    if line.startswith("Ticker,Company") or line.startswith("#"):
        continue
    parts = line.split(',', 1) # Разделяем только по первой запятой
    if len(parts) == 2:
        ticker = parts[0].strip()
        company_name = parts[1].strip()
        if ticker and ticker not in ticker_to_company_map: # Добавляем, если тикер еще не встречался
            ticker_to_company_map[ticker] = company_name
            ordered_tickers.append(ticker)
# Если нужны только уникальные тикеры в определенном порядке, можно оставить ordered_tickers
# Если порядок не важен, можно просто итерироваться по ticker_to_company_map.keys()
# Для сохранения оригинального порядка (минус дубликаты) используем ordered_tickers

# Даты
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=5*365 + 1) # Примерно 3 года ( +1 на всякий случай для полноты)

all_stock_data_yf = []

print(f"Загрузка данных с {start_date.strftime('%Y-%m-%d')} по {end_date.strftime('%Y-%m-%d')} используя yfinance.")
print(f"Будет обработано {len(ordered_tickers)} тикеров.")

for i, symbol in enumerate(ordered_tickers):
    company_name = ticker_to_company_map.get(symbol, "N/A") # Получаем имя компании, если нет - "N/A"
    print(f"\n({i+1}/{len(ordered_tickers)}) Получение данных для: {symbol} ({company_name})...")
    try:
        ticker_obj = yf.Ticker(symbol)
        hist_data = ticker_obj.history(start=start_date.strftime('%Y-%m-%d'),
                                       end=end_date.strftime('%Y-%m-%d'),
                                       interval="1d",
                                       # actions=False # Чтобы не загружать дивиденды и сплиты, если не нужны
                                       auto_adjust=False # Важно для получения 'Close' а не 'Adj Close' по умолчанию
                                      )


        if not hist_data.empty:
            hist_data.reset_index(inplace=True)
            hist_data['ticker'] = symbol
            hist_data['company_name'] = company_name # Добавляем название компании

            # Переименовываем колонки
            hist_data.rename(columns={
                'Date': 'date',
                'Open': 'o',
                'High': 'h',
                'Low': 'l',
                'Close': 'c' # yfinance по умолчанию дает 'Close', если auto_adjust=False
            }, inplace=True)

            # Преобразуем дату в строку YYYY-MM-DD
            # Убедимся, что колонка 'date' имеет тип datetime перед форматированием
            hist_data['date'] = pd.to_datetime(hist_data['date']).dt.strftime('%Y-%m-%d')

            # Рассчитываем 'pc' (Previous Close)
            hist_data['pc'] = hist_data['c'].shift(1)

            # Рассчитываем 'd' (Change) и 'dp' (Percent Change)
            hist_data['d'] = None
            hist_data['dp'] = None

            valid_pc_indices = hist_data['pc'].notna() & (hist_data['pc'] != 0)
            hist_data.loc[valid_pc_indices, 'd'] = hist_data.loc[valid_pc_indices, 'c'] - hist_data.loc[valid_pc_indices, 'pc']
            hist_data.loc[valid_pc_indices, 'dp'] = (hist_data.loc[valid_pc_indices, 'd'] / hist_data.loc[valid_pc_indices, 'pc']) * 100

            # Выбираем нужные колонки, включая company_name
            df_selected = hist_data[['ticker', 'company_name', 'date', 'o', 'h', 'l', 'c', 'pc', 'd', 'dp']]
            all_stock_data_yf.extend(df_selected.to_dict('records'))
            print(f"  Данные для {symbol} ({company_name}) успешно получены ({len(df_selected)} записей).")
        else:
            print(f"  Нет данных для {symbol} ({company_name}) за указанный период.")

    except Exception as e:
        print(f"  Произошла ошибка при обработке {symbol} ({company_name}): {e}")
    
    time.sleep(0.6) # Небольшая задержка

if all_stock_data_yf:
    output_df_yf = pd.DataFrame(all_stock_data_yf)
    
    # Округление числовых значений
    float_cols = ['o', 'h', 'l', 'c', 'pc', 'd', 'dp']
    for col in float_cols:
        if col in output_df_yf.columns:
             output_df_yf[col] = pd.to_numeric(output_df_yf[col], errors='coerce').round(4)

    csv_filename_yf = "stock_data_3years_yfinance_with_names.csv"
    output_df_yf.to_csv(csv_filename_yf, index=False, encoding='utf-8-sig')
    print(f"\nВсе данные успешно собраны и сохранены в файл: {csv_filename_yf}")
else:
    print("\nНе удалось собрать данные ни для одного тикера с помощью yfinance.")