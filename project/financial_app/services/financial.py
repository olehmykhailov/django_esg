import csv
import re
from financial_app.models import FinancialData


class FinancialETL:
    def __init__(self, file):
        self.file = file

    def clean_key(self, key):
        """Clean column names to match model fields"""
        key = key.strip().lower()
        key = re.sub(r"[^\w]", "_", key)
        key = re.sub(r"_+", "_", key)
        return key.strip("_")

    def extract(self):
        """Extract data from CSV file"""
        self.file.seek(0)
        decoded = self.file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded)
        data = []
        for row in reader:
            new_row = {
                self.clean_key(k): v for k, v in row.items()
                if v and v.strip()
            }
            data.append(new_row)
        return data

    def transform(self, data):
        """Transform data to match model requirements"""
        for row in data:
            # Clean numeric values
            for key in ['fixed_costs', 'variable_costs', 'sales_revenue', 'gross_margin', 
                       'operating_margin', 'operating_profit', 'net_profit', 'equity', 
                       'liabilities', 'roa', 'roe', 'current_ratio', 'debt_ratio', 'asset_turnover']:
                if key in row and row[key]:
                    row[key] = row[key].replace(",", ".")
        return data

    def load(self, data):
        """Load data into database"""
        for row in data:
            FinancialData.objects.create(
                ticker=row.get('company', ''),
                year=int(row.get('year', 0)),
                fixed_costs=float(row.get('fixed_costs', 0)) if row.get('fixed_costs') else None,
                variable_costs=float(row.get('variable_costs', 0)) if row.get('variable_costs') else None,
                units_sold=int(row.get('units_sold', 0)) if row.get('units_sold') else None,
                sales_revenue=float(row.get('sales_revenue', 0)) if row.get('sales_revenue') else None,
                gross_margin=float(row.get('gross_margin', 0)) if row.get('gross_margin') else None,
                operating_margin=float(row.get('operating_margin', 0)) if row.get('operating_margin') else None,
                operating_profit=float(row.get('operating_profit', 0)) if row.get('operating_profit') else None,
                net_profit=float(row.get('net_profit', 0)) if row.get('net_profit') else None,
                equity=float(row.get('equity', 0)) if row.get('equity') else None,
                liabilities=float(row.get('liabilities', 0)) if row.get('liabilities') else None,
                roa=float(row.get('roa', 0)) if row.get('roa') else None,
                roe=float(row.get('roe', 0)) if row.get('roe') else None,
                current_ratio=float(row.get('current_ratio', 0)) if row.get('current_ratio') else None,
                debt_ratio=float(row.get('debt_ratio', 0)) if row.get('debt_ratio') else None,
                asset_turnover=float(row.get('asset_turnover', 0)) if row.get('asset_turnover') else None,
            )

    def run(self):
        """Run the complete ETL process"""
        raw_data = self.extract()
        cleaned_data = self.transform(raw_data)
        self.load(cleaned_data)
        print("Financial data ETL completed successfully")



