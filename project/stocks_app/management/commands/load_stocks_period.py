from django.core.management.base import BaseCommand
from stocks_app.services.stock_service import run

class Command(BaseCommand):
    help = 'Load stock data for specific period'

    def add_arguments(self, parser):
        parser.add_argument('--ticker', type=str, help='Stock ticker')
        parser.add_argument('--start', type=str, default='2024-05-01')
        parser.add_argument('--end', type=str, default='2025-05-31')

    def handle(self, *args, **options):
        ticker = options['ticker']
        start_date = options['start']
        end_date = options['end']
        
        if ticker:
            self.stdout.write(f'Loading {ticker} from {start_date} to {end_date}...')
            try:
                run(ticker, start_date, end_date)
                self.stdout.write(self.style.SUCCESS(f'✅ {ticker} loaded successfully'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error: {e}'))
        else:
            self.stdout.write(self.style.ERROR('Please provide --ticker argument'))
