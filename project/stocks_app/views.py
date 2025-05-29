from django.shortcuts import render
from stocks_app.services.stock_service import run

# Create your views here.
def upload_stocks(request):
    if request.method == 'POST':
        ticker = request.POST.get("ticker")
        date_from = request.POST.get("date_from")
        date_to = request.POST.get("date_to")
        try:
            run(ticker, date_from, date_to)
            
            return render(request, 'upload_stocks.html', {'success': True})
        except Exception as e:
            return render(request, 'upload_stocks.html', {'error': str(e)})
    return render(request, 'upload_stocks.html')