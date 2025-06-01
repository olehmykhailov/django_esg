from django.shortcuts import render
from stocks_app.services.stock_service import run, transform_stock_data, get_stock_data
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime
from stocks_app.models import StocksData, Predict

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

@csrf_exempt
@require_http_methods(["POST"])
def save_predict(request):
    """
    API endpoint to save prediction data.
    Expected JSON: {"ticker": "AAPL", "close": 150.25, "date": "2024-01-15"}
    """
    try:
        data = json.loads(request.body)
        ticker = data.get('ticker')
        close = data.get('close')
        date_str = data.get('date')
        
        if not all([ticker, close, date_str]):
            return JsonResponse({'error': 'Missing required fields: ticker, close, date'}, status=400)
        
        
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
        
        
        predict, created = Predict.objects.update_or_create(
            ticker=ticker,
            date=date_obj,
            defaults={'close': close}
        )
        
        return JsonResponse({
            'success': True,
            'id': predict.id,
            'created': created
        }, status=201 if created else 200)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_real_data(request):
    """
    API endpoint to get real stock data for a period.
    Query params: ticker, date_from, date_to
    """
    ticker = request.GET.get('ticker')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if not all([ticker, date_from, date_to]):
        return JsonResponse({'error': 'Missing required params: ticker, date_from, date_to'}, status=400)
    
    try:
        
        date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
        date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()

        try:
            run(ticker, date_from, date_to)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        
        real_data = StocksData.objects.filter(
            ticker=ticker,
            date__gte=date_from_obj,
            date__lte=date_to_obj
        ).order_by('date').values('date', 'close', 'open', 'high', 'low', 'volume')
        
        return JsonResponse({
            'ticker': ticker,
            'data': list(real_data)
        })
        
    except ValueError:
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)