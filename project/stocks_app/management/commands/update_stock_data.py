from django.core.management.base import BaseCommand
from stocks_app.services.stock_service import get_stock_data, transform_stock_data, load_stock_data
from stocks_app.models import StocksData
from datetime import date, timedelta, datetime

class Command(BaseCommand):
    help = 'Update stock data for all tickers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Specific date to update (YYYY-MM-DD format)',
        )

    def handle(self, *args, **options):
        if options['date']:
            try:
                target_date = datetime.strptime(options['date'], '%Y-%m-%d').date()
            except ValueError:
                self.stdout.write(self.style.ERROR('Invalid date format. Use YYYY-MM-DD'))
                return
        else:
            target_date = date.today() - timedelta(days=1)
        
        date_str = target_date.strftime('%Y-%m-%d')
        
        tickers = StocksData.objects.values_list('ticker', flat=True).distinct()
        
        self.stdout.write(f'Updating stock data for {len(tickers)} tickers on {date_str}...')
        
        updated_count = 0
        for ticker in tickers:
            try:
                if StocksData.objects.filter(ticker=ticker, date=target_date).exists():
                    self.stdout.write(f'Data for {ticker} on {date_str} already exists. Skipping.')
                    continue

                df = get_stock_data(ticker, date_str, date_str)
                if df.empty:
                    self.stdout.write(f'No data available for {ticker} on {date_str}')
                    continue

                df_transformed = transform_stock_data(df)
                load_stock_data(df_transformed, ticker)
                
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f' Updated {ticker}'))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error updating {ticker}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'Stock data update completed! Updated {updated_count} tickers.'))
