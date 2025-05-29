import csv
from datetime import datetime
import re
from etl_app.models import GreenhouseData, EnergyData, Metadata, DiversityData


class BaseETL:
    def __init__(self, company, file):
        self.company = company
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
        print(cleaned)
        self.load(cleaned)
        print(f"✅ Завершено ETL для {type(self).__name__}")

class MetadataETL(BaseETL):
    def transform(self, data):
        for row in data:

            row["year"] = datetime.strptime(row["year"], "%Y").year
            row["value"] = row["value"].replace(",", ".")
        
        return data

    def load(self, data):
        for row in data:
            Metadata.objects.create(
                company=self.company,
                category=row["category"],
                subcategory=row["subcategory"],
                metric=row["metric"],
                year=int(row["year"]),
                value=float(row["value"])
            )

class GreenhouseETL(BaseETL):
    def transform(self, data):
        for row in data:
            try:
                row["value"] = row["value"].replace(",", ".")
            except KeyError:
                row["value"] = "0"
                
        
        return data

    def load(self, data):
        for row in data:
            GreenhouseData.objects.create(
                company=self.company,
                category=row["category"],
                subcategory=row["subcategory"],
                metric=row["metric"],
                year=int(row["year"]),
                value=float(row["value"])
            )

class EnergyETL(BaseETL):
    def transform(self, data):
        for row in data:
            row["value"] = row["value"].replace(",", ".")
        return data

    def load(self, data):
        for row in data:
            EnergyData.objects.create(
                company=self.company,
                category=row["category"],
                subcategory=row["subcategory"],
                metric=row["metric"],
                unit=row["unit"],
                year=int(row["year"]),
                value=float(row["value"])
            )

class DiversityETL(BaseETL):
    def transform(self, data):
        for row in data:
            for key in ["women_in_workforce", "black_employees", "latino_employees", "asian_employees", "multiracial_employees"]:
                if key in row:
                    row[key] = row[key].replace(",", ".")
        return data

    def load(self, data):
        for row in data:
            DiversityData.objects.create(
                company=self.company,
                year=int(row["year"]),
                women_in_workforce=float(row.get("women_in_workforce", 0)),
                black_employees=float(row.get("black_employees", 0)),
                latino_employees=float(row.get("latino_employees", 0)),
                asian_employees=float(row.get("asian_employees", 0)),
                multiracial_employees=float(row.get("multiracial_employees", 0)),
            )