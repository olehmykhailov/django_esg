from django.shortcuts import render
import pandas as pd
from etl_app.services.etl import (
    GreenhouseETL,
    EnergyETL,
    MetadataETL,
    DiversityETL,
)

def handle_upload(request, template_name, etl_class):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        company = str(request.POST.get("company"))
        ticker = str(request.POST.get("ticker"))  # ← додаємо це
        category = str(request.POST.get("category"))  # ← додаємо це
        file = request.FILES["csv_file"]
        confirm = request.POST.get("confirm")

        if confirm:
            try:
                # Якщо це MetadataETL, передаємо category
                if etl_class.__name__ == 'MetadataETL':
                    etl = etl_class(company.lower(), file, category.lower(), ticker.lower())
                else:
                    etl = etl_class(company.lower(), file, ticker.lower())

                etl.run()
                return render(request, template_name, {
                    'success': True,
                    'message': '✅ Дані успішно завантажено до БД',
                    'company': company,
                    'ticker': ticker,
                    'category': category
                })
            except Exception as e:
                return render(request, template_name, {
                    'error': str(e),
                    'company': company,
                    'category': category
                })

        # CSV preview:
        try:
            df = pd.read_csv(file)
            preview_html = df.head(10).to_html(classes='table table-bordered', index=False)
            return render(request, template_name, {
                'preview': preview_html,
                'company': company,
                'category': category,
                'file': file,
                'confirm_required': True
            })
        except Exception as e:
            return render(request, template_name, {'error': str(e)})

    return render(request, template_name)



def upload_greenhouse(request):
    return handle_upload(request, 'upload_greenhouse.html', GreenhouseETL)

def upload_energy(request):
    return handle_upload(request, 'upload_energy.html', EnergyETL)

def upload_metadata(request):
    return handle_upload(request, 'upload_metadata.html', MetadataETL)

def upload_diversity(request):
    return handle_upload(request, 'upload_diversity.html', DiversityETL)
