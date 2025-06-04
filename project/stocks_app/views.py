from django.shortcuts import render
from stocks_app.services.stock_service import run, transform_stock_data, get_stock_data
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime, date
from django.core.serializers.json import DjangoJSONEncoder
from stocks_app.models import StocksData, Predict

def upload_stocks(request):
    if request.method == 'POST':
        ticker = request.POST.get("ticker")
        date_from = request.POST.get("date_from")
        date_to = request.POST.get("date_to")
        
        try:
            df = get_stock_data(ticker, date_from, date_to)
            df_transformed = transform_stock_data(df)
            preview_html = df_transformed.head(10).to_html(classes='table table-striped', index=False)
            
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

@csrf_exempt
@require_http_methods(["POST"])
def save_predict_batch(request):
    try:
        data = json.loads(request.body)
        predictions = data.get('predictions', [])
        
        if not predictions:
            return JsonResponse({'error': 'No predictions provided'}, status=400)
        
        results = []
        for pred in predictions:
            ticker = pred.get('ticker')
            close = pred.get('close')
            date_str = pred.get('date')
            
            if not all([ticker, close, date_str]):
                results.append({
                    'ticker': ticker,
                    'error': 'Missing required fields: ticker, close, date'
                })
                continue
            
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                results.append({
                    'ticker': ticker,
                    'error': 'Invalid date format. Use YYYY-MM-DD'
                })
                continue
            
            try:
                predict, created = Predict.objects.update_or_create(
                    ticker=ticker,
                    date=date_obj,
                    defaults={'close': close}
                )
                
                results.append({
                    'ticker': ticker,
                    'id': predict.id,
                    'created': created,
                    'success': True
                })
            except Exception as e:
                results.append({
                    'ticker': ticker,
                    'error': str(e)
                })
        
        return JsonResponse({'results': results}, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_real_data(request):
    ticker = request.GET.get('ticker')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if not all([ticker, date_from, date_to]):
        return JsonResponse({'error': 'Missing required params: ticker, date_from, date_to'}, status=400)
    
    try:
        date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
        date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
        
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

def stock_chart(request, ticker):
    from datetime import timedelta
    end_date = date.today() + timedelta(days=7)
    start_date = date.today() - timedelta(days=60)
    
    real_data = StocksData.objects.filter(
        ticker=ticker,
        date__gte=start_date,
        date__lt=date.today()
    ).order_by('date').values('date', 'close')
    
    predict_data = Predict.objects.filter(
        ticker=ticker,
        date__gte=start_date,
        date__lte=end_date
    ).order_by('date').values('date', 'close', 'created_at')
    
    real_data_list = []
    for item in real_data:
        real_data_list.append({
            'date': item['date'].isoformat(),
            'close': float(item['close'])
        })
    
    predict_data_list = []
    for item in predict_data:
        predict_data_list.append({
            'date': item['date'].isoformat(),
            'close': float(item['close']),
            'created_at': item['created_at'].isoformat()
        })
    
    latest_prediction = Predict.objects.filter(
        ticker=ticker
    ).order_by('-date', '-created_at').first()
    
    today_real = StocksData.objects.filter(
        ticker=ticker,
        date=date.today()
    ).first()
    
    context = {
        'ticker': ticker,
        'real_data': json.dumps(real_data_list),
        'predict_data': json.dumps(predict_data_list),
        'latest_prediction': latest_prediction,
        'today_real': today_real,
        'current_date': date.today().isoformat()
    }
    
    return render(request, 'stock_chart.html', context)

@require_http_methods(["GET"])
def get_chart_data(request, ticker):
    from datetime import timedelta
    
    end_date = date.today() + timedelta(days=7)
    start_date = date.today() - timedelta(days=60)
    
    real_data = StocksData.objects.filter(
        ticker=ticker,
        date__gte=start_date,
        date__lte=date.today()
    ).order_by('date').values('date', 'close')
    
    predict_data = Predict.objects.filter(
        ticker=ticker,
        date__gte=start_date,
        date__lte=end_date
    ).order_by('date').values('date', 'close', 'created_at')
    
    real_data_list = []
    for item in real_data:
        real_data_list.append({
            'date': item['date'].isoformat(),
            'close': float(item['close'])
        })
    
    predict_data_list = []
    for item in predict_data:
        predict_data_list.append({
            'date': item['date'].isoformat(),
            'close': float(item['close']),
            'created_at': item['created_at'].isoformat()
        })
    
    latest_prediction = Predict.objects.filter(
        ticker=ticker
    ).order_by('-date', '-created_at').first()
    
    latest_pred_data = None
    if latest_prediction:
        latest_pred_data = {
            'date': latest_prediction.date.isoformat(),
            'close': float(latest_prediction.close),
            'created_at': latest_prediction.created_at.isoformat()
        }
    
    return JsonResponse({
        'real_data': real_data_list,
        'predict_data': predict_data_list,
        'latest_prediction': latest_pred_data,
        'last_updated': datetime.now().isoformat()
    })

def ticker_list(request):
    tickers = StocksData.objects.values_list('ticker', flat=True).distinct().order_by('ticker')
    return render(request, 'ticker_list.html', {'tickers': tickers})

def home(request):
    return render(request, 'home.html')

@require_http_methods(["GET"])
def get_all_tickers_data(request):
    target_date = request.GET.get('date')
    
    if not target_date:
        return JsonResponse({'error': 'Missing required param: date'}, status=400)
    
    try:
        date_obj = datetime.strptime(target_date, '%Y-%m-%d').date()
        
        data = StocksData.objects.filter(
            date=date_obj
        ).values('ticker', 'date', 'close', 'open', 'high', 'low', 'volume')
        
        return JsonResponse({
            'date': target_date,
            'count': len(data),
            'data': list(data)
        })
        
    except ValueError:
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_ticker_latest(request, ticker):
    try:
        latest = StocksData.objects.filter(
            ticker=ticker
        ).order_by('-date').first()
        
        if not latest:
            return JsonResponse({'error': f'No data found for ticker {ticker}'}, status=404)
        
        return JsonResponse({
            'ticker': ticker,
            'date': latest.date.isoformat(),
            'close': float(latest.close),
            'open': float(latest.open),
            'high': float(latest.high),
            'low': float(latest.low),
            'volume': latest.volume
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)