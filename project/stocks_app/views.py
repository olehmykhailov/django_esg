from django.shortcuts import render
from stocks_app.services.stock_service import run, transform_stock_data, get_stock_data

# Create your views here.
def upload_stocks(request):
    if request.method == 'POST':
        ticker = request.POST.get("ticker")
        date_from = request.POST.get("date_from")
        date_to = request.POST.get("date_to")
        
        try:
            # Get and transform data
            df = get_stock_data(ticker, date_from, date_to)
            df_transformed = transform_stock_data(df)
            preview_html = df_transformed.head(10).to_html(classes='table table-striped', index=False)
            
            # Run ETL
            run(ticker, date_from, date_to)
            
            return render(request, 'upload_stocks.html', {
                'success': True,
                'preview': preview_html
            })
        except Exception as e:
            return render(request, 'upload_stocks.html', {'error': str(e)})
    return render(request, 'upload_stocks.html')