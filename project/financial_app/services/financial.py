import re
import csv
from financial_app.models import FinancialData

class BaseETL:
    def __init__(self, file):
        self.file = file

    def clean_key(self, key):
        key = key.strip().lower()
        key = re.sub(r"\s*\(\s*%\s*\)", "", key)
        key = re.sub(r"[^\w]", "_", key)
        key = re.sub(r"_+", "_", key)
        return key.strip("_")

    def extract(self):
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
        return data

    def load(self, data):
        raise NotImplementedError

    def run(self):
        raw = self.extract()
        cleaned = self.transform(raw)
        self.load(cleaned)
        print(f"✅ Завершено ETL для {type(self).__name__}")

class FinancialETL(BaseETL):
    def transform(self, data):
        for row in data:
            for key, value in row.items():
                print(f"🔍 Перевірка поля {key} {row[key]}")
                
                if value is None or value == "":
                    print(f"❌ Пропущено поле {key} у рядка {row}")
                    continue
                
                if isinstance(value, str) and "," in value:
                    row[key] = value.replace(",", ".")
        return data
    @staticmethod
    def to_float(val):
        try:
            return float(val)
        except (TypeError, ValueError):
            return None
    @staticmethod
    def to_int(val):
        try:
            return int(val)
        except (TypeError, ValueError):
            return None


    def load(self, data):
        for row in data:
            try:
                FinancialData.objects.create(
                    ticker=row.get("ticker"),
                    fixed_costs=self.to_float(row.get("fixed_costs")),
                    variable_costs=self.to_float(row.get("variable_costs")),
                    units_sold=self.to_int(row.get("units_sold")),
                    sales_revenue=self.to_float(row.get("sales_revenue")),
                    gross_margin=self.to_float(row.get("gross_margin")),
                    operating_margin=self.to_float(row.get("operating_margin")),
                    operating_profit=self.to_float(row.get("operating_profit")),
                    net_profit=self.to_float(row.get("net_profit")),
                    equity=self.to_float(row.get("equity")),
                    liabilities=self.to_float(row.get("liabilities")),
                    roa=self.to_float(row.get("roa")),
                    roe=self.to_float(row.get("roe")),
                    current_ratio=self.to_float(row.get("current_ratio")),
                    debt_ratio=self.to_float(row.get("debt_ratio")),
                    asset_turnover=self.to_float(row.get("asset_turnover")),
                    year=self.to_int(row.get("year"))
                )
            except Exception as e:
                print(f"❌ Помилка при завантаженні рядка {row}: {e}")
                raise e



