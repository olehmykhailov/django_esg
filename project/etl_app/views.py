from django.shortcuts import render
from etl_app.services.etl import ( 
    GreenhouseETL,
    EnergyETL,
    MetadataETL,
    DiversityETL,
)

def upload_greenhouse(request):
    if request.method == 'POST':
        company = request.POST.get("company")
        file = request.FILES.get('csv_file')
        try:
            etl = GreenhouseETL(company, file)
            etl.run()
            return render(request, 'upload_greenhouse.html', {'success': True})
        except Exception as e:
            return render(request, 'upload_greenhouse.html', {'error': str(e)})
    return render(request, 'upload_greenhouse.html')

def upload_energy(request):
    if request.method == 'POST':
        company = request.POST.get("company")
        file = request.FILES.get('csv_file')
        try:
            etl = EnergyETL(company, file)
            etl.run()
            return render(request, 'upload_energy.html', {'success': True})
        except Exception as e:
            return render(request, 'upload_energy.html', {'error': str(e)})
    return render(request, 'upload_energy.html')

def upload_metadata(request):
    if request.method == 'POST':
        company = request.POST.get("company")
        file = request.FILES.get('csv_file')
        try:
            etl = MetadataETL(company, file)
            etl.run()
            return render(request, 'upload_metadata.html', {'success': True})
        except Exception as e:
            return render(request, 'upload_metadata.html', {'error': str(e)})
    return render(request, 'upload_metadata.html')\
    
def upload_diversity(request):
    if request.method == 'POST':
        company = request.POST.get("company")
        file = request.FILES.get('csv_file')
        try:
            etl = DiversityETL(company, file)
            etl.run()
            return render(request, 'upload_diversity.html', {'success': True})
        except Exception as e:
            return render(request, 'upload_diversity.html', {'error': str(e)})
    return render(request, 'upload_diversity.html')
