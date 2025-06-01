import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import timedelta
from stocks_app.models import StocksData

def generate_diversity_pie_chart(data_obj):
    labels = ['Women', 'Black', 'Latino', 'Asian', 'Multiracial']
    sizes = [
        data_obj.women_in_workforce,
        data_obj.black_employees,
        data_obj.latino_employees,
        data_obj.asian_employees,
        data_obj.multiracial_employees
    ]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode('utf-8')


import matplotlib.pyplot as plt
from datetime import timedelta
from io import BytesIO
import base64
from stocks_app.models import StocksData  # если это нужно

def generate_market_reaction_chart(events, label, ticker):
    fig, ax = plt.subplots()

    for event in events:
        print(event.category)
        center = event.date_of_publication
        start = center - timedelta(days=90)
        end = center + timedelta(days=90)

        stock_data = StocksData.objects.filter(
            ticker=ticker,
            date__range=(start, end)
        ).order_by('date')

        if stock_data.exists():
            dates = [d.date for d in stock_data]
            prices = [d.close for d in stock_data]

            # Построить линию цены
            ax.plot(dates, prices, label="Close price", color='black')  # например, черная линия


            # Добавить вертикальную метку события
            color = 'red' if event.category == 'financial_report' else 'blue'
            ax.axvline(center, color=color, linestyle='--', alpha=0.6)



    ax.set_title(f'{label} Report Reaction')
    ax.set_xlabel('Date')
    ax.set_ylabel('Close Price')
    ax.legend(fontsize=6)
    fig.autofmt_xdate()
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

