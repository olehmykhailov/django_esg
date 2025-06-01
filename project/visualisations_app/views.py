from django.shortcuts import render
from etl_app.models import DiversityData
from etl_app.models import Metadata
from visualisations_app.services.charts import generate_diversity_pie_chart, generate_market_reaction_chart

def render_dashboard(request):
    company = str(request.GET.get('company')).lower()
    ticker = str(request.GET.get('ticker')).lower()
    year = int(request.GET.get('year', 0))
    print(f"Rendering dashboard for company: {company}, ticker: {ticker}, year: {year}")
    diversity_img = None
    fin_chart_img = None
    esg_chart_img = None

    if company and ticker and year:
        try:
            ddata = DiversityData.objects.get(company=company, year=year)
            diversity_img = generate_diversity_pie_chart(ddata)
        except DiversityData.DoesNotExist:
            pass

        fin_events = Metadata.objects.filter(ticker=ticker, year=year, category__icontains="financial")
        esg_events = Metadata.objects.filter(ticker=ticker, year=year, category__icontains="esg")
        print(fin_events.count(), esg_events.count())
        
        if fin_events.exists():
            fin_chart_img = generate_market_reaction_chart(fin_events, "Financial", ticker)
        if esg_events.exists():
            esg_chart_img = generate_market_reaction_chart(esg_events, "ESG", ticker)

    return render(request, 'dashboard.html', {
        'diversity_img': diversity_img,
        'fin_chart_img': fin_chart_img,
        'esg_chart_img': esg_chart_img,
        'company': company,
        'ticker': ticker,
        'year': year,
    })
