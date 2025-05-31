from django.shortcuts import render
import pandas as pd
from financial_app.services.financial import FinancialETL

def handle_upload(request, template_name, etl_class):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        company = request.POST.get("ticker")
        file = request.FILES["csv_file"]
        confirm = request.POST.get("confirm")

        if confirm:
            try:
                etl = etl_class(file)
                etl.run()
                return render(request, template_name, {
                    'success': True,
                    'message': '✅ Data successfully uploaded to the database',
                    'company': company,
                })
            except Exception as e:
                return render(request, template_name, {
                    'error': str(e),
                    'company': company,
                })

        try:
            df = pd.read_csv(file)
            preview_html = df.head(10).to_html(classes='table table-bordered', index=False)
            return render(request, template_name, {
                'preview': preview_html,
                'company': company,
                'file': file,
                'confirm_required': True
            })
        except Exception as e:
            return render(request, template_name, {'error': str(e)})

    return render(request, template_name)


def upload_financial_data(request):
    return handle_upload(request, 'upload_financial_data.html', FinancialETL)