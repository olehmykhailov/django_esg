from django.shortcuts import render
from .services.visualisation_service.data_loader import load_stock_df, load_ghg_df, load_diversity_df, load_energy_df
from .services.visualisation_service.data_processing import merge_indicator_with_stock
from .services.visualisation_service.events import get_sample_events, get_covid_periods
from .services.visualisation_service.pallette import dashboard_palette
from .services.visualisation_service.charts import (
    plot_stock_with_events,
    plot_ghg_scopes_stacked,
    plot_diversity_pie,
    plot_total_energy_line,
    plot_fuel_mix_stacked,
    create_kpi_card
)


def dashboard_view(request):
    stock_df = load_stock_df()
    ghg_df = load_ghg_df()
    diversity_df = load_diversity_df()
    energy_df = load_energy_df()
    events = get_sample_events()
    covid = get_covid_periods()

    charts = {
        'stock': plot_stock_with_events(stock_df, events, covid, dashboard_palette),
        'ghg': plot_ghg_scopes_stacked(ghg_df, dashboard_palette),
        'diversity': plot_diversity_pie(diversity_df, dashboard_palette),
        'energy_total': plot_total_energy_line(energy_df, dashboard_palette),
        'fuel_mix': plot_fuel_mix_stacked(energy_df),
        'kpi_ghg': create_kpi_card("25.4 Mt", "Total GHG Emissions", "-3.2% vs PY", change_color="green", dashboard_palette=dashboard_palette),
        'kpi_women': create_kpi_card("42%", "Women in Workforce", "+1% vs PY", change_color="green", dashboard_palette=dashboard_palette),
    }

    return render(request, "dashboard.html", charts)
