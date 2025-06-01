from datetime import datetime

def get_covid_periods():
    return [{'start': datetime(2020, 3, 1), 'end': datetime(2021, 6, 30), 'label': 'COVID-19 Impact', 'color': '#FEF3C7', 'alpha': 0.3}]


def get_sample_events():
    return [
        {'date': datetime(2020, 6, 22), 'label': 'WWDC20', 'color': '#A78BFA', 'linestyle': ':'},
        {'date': datetime(2021, 9, 14), 'label': 'iPhone13', 'color': '#A78BFA', 'linestyle': ':'},
        {'date': datetime(2023, 6, 5), 'label': 'VisionPro Ann.', 'color': '#A78BFA', 'linestyle': ':'},
    ]