import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import timedelta
from .plot_helpers import format_dashboard_plot, fig_to_base64
import numpy as np

# --- Stock Price with Events ---
def plot_stock_with_events(stock_df, all_events, covid_periods, dashboard_palette):
    fig, ax = plt.subplots(figsize=(18, 9))
    ax.plot(stock_df.index, stock_df['close'], color=dashboard_palette['stock_price_line'], linewidth=1.2)
    ax.fill_between(stock_df.index, stock_df['close'], alpha=0.15, color=dashboard_palette['stock_price_line'])

    y_min, y_max = ax.get_ylim()
    y_positions = list(np.linspace(y_max, y_min, num=6))

    for idx, event in enumerate(sorted(all_events, key=lambda x: x['date'])):
        if stock_df.index.min() <= event['date'] <= stock_df.index.max():
            ax.axvline(event['date'], color=event['color'], linestyle=event['linestyle'], linewidth=1, alpha=0.7)
            ax.text(event['date'] + timedelta(days=4), y_positions[idx % len(y_positions)], event['label'], rotation=90,
                    verticalalignment='bottom', horizontalalignment='left', fontsize=7.5, color=event['color'], alpha=0.9, weight='semibold')

    for period in covid_periods:
        ax.axvspan(period['start'], period['end'], color=period['color'], alpha=period['alpha'], zorder=0, label=period['label'])

    format_dashboard_plot(fig, ax, title='Apple (AAPL) Stock Price & Key Events', ylabel_left='Closing Price (USD)', axis_color_left=dashboard_palette['stock_price_line'])
    plt.tight_layout()
    return fig_to_base64(fig)

# --- GHG Stacked Scopes ---
def plot_ghg_scopes_stacked(ghg_df, dashboard_palette):
    scope1 = ghg_df[ghg_df['Subcategory'] == 'Scope 1'].groupby('year')['Value'].sum()
    scope2 = ghg_df[ghg_df['Subcategory'] == 'Scope 2'].groupby('year')['Value'].sum()
    scope3 = ghg_df[ghg_df['Subcategory'] == 'Gross emissions (Scope 3)'].groupby('year')['Value'].sum()
    df = pd.DataFrame({'Scope 1': scope1, 'Scope 2': scope2, 'Scope 3': scope3}).fillna(0).reset_index()
    if df.empty:
        return None
    fig, ax = plt.subplots(figsize=(10, 6))
    df.set_index('year').plot(kind='bar', stacked=True, ax=ax, color=[dashboard_palette['scope1'], dashboard_palette['scope2'], dashboard_palette['scope3']])
    format_dashboard_plot(fig, ax, 'GHG Emissions by Scope', ylabel_left='Emissions (Mt CO2e)', axis_color_left=dashboard_palette['text_body'])
    plt.tight_layout()
    return fig_to_base64(fig)

# --- Diversity Pie Chart ---
def plot_diversity_pie(diversity_df, dashboard_palette):
    last_year = diversity_df['year'].max()
    row = diversity_df[diversity_df['year'] == last_year]
    if row.empty:
        return None
    data = {
        'Black': row['Black_Employees'].iloc[0],
        'Latino': row['Latino_Employees'].iloc[0],
        'Asian': row['Asian_Employees'].iloc[0],
        'Multiracial': row['Multiracial_Employees'].iloc[0]
    }
    labels = list(data.keys())
    sizes = [v * 100 for v in data.values()]
    colors = [dashboard_palette['pie_1'], dashboard_palette['pie_2'], dashboard_palette['pie_3'], dashboard_palette['pie_4']]
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%', startangle=90, wedgeprops=dict(width=0.4))
    ax.axis('equal')
    fig.suptitle(f'Workforce Ethnic Diversity ({last_year})', fontsize=14, color=dashboard_palette['text_header'])
    return fig_to_base64(fig)

# --- Correlation Chart ---
def plot_correlation_dashboard(df_merged, esg_col, esg_label, stock_col, stock_label, title, esg_color_val, stock_color_val, dashboard_palette, bar_plot_esg=True):
    if df_merged.empty:
        return None
    fig, ax1 = plt.subplots(figsize=(10, 5.5))
    if bar_plot_esg:
        sns.barplot(x='year', y=esg_col, data=df_merged, ax=ax1, color=esg_color_val)
    else:
        sns.lineplot(x='year', y=esg_col, data=df_merged, ax=ax1, color=esg_color_val, marker='o')

    ax2 = ax1.twinx()
    ax2.plot(df_merged['year'], df_merged[stock_col], color=stock_color_val, marker='.', linewidth=2)
    format_dashboard_plot(fig, ax1, title, xlabel='Year', ylabel_left=esg_label, axis_color_left=esg_color_val, suptitle_mode=True)
    plt.tight_layout()
    return fig_to_base64(fig)

# --- KPI Card ---
def create_kpi_card(value_str, label_str, change_str=None, change_color='green', card_bg_color='#FFFFFF', text_color_val='#000000', dashboard_palette=None):
    fig, ax = plt.subplots(figsize=(3, 2.2))
    fig.patch.set_facecolor(dashboard_palette['background_figure'] if dashboard_palette else '#FFFFFF')
    ax.set_facecolor(card_bg_color)
    ax.text(0.5, 0.60, value_str, ha='center', va='center', fontsize=22, weight='semibold', color=text_color_val)
    ax.text(0.5, 0.28, label_str, ha='center', va='center', fontsize=9, color=dashboard_palette['text_body'] if dashboard_palette else '#555555')
    if change_str:
        ax.text(0.5, 0.10, change_str, ha='center', va='center', fontsize=8, color=change_color)
    ax.set_axis_off()
    plt.tight_layout()
    return fig_to_base64(fig)

# --- Market Reaction Chart ---
def plot_market_reaction_dashboard(stock_df, publication_date, event_name, dashboard_palette, window_days=30):
    start = publication_date - timedelta(days=window_days)
    end = publication_date + timedelta(days=window_days)
    window_df = stock_df[(stock_df.index >= start) & (stock_df.index <= end)]
    if window_df.empty:
        return None
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(window_df.index, window_df['close'], color=dashboard_palette['stock_price_line'], linewidth=2)
    ax.axvline(publication_date, color=dashboard_palette['event_esg'], linestyle='--')
    format_dashboard_plot(fig, ax, f'Stock Price Reaction: {event_name}', ylabel_left='Stock Price (USD)', axis_color_left=dashboard_palette['stock_price_line'], suptitle_mode=True)
    plt.tight_layout()
    return fig_to_base64(fig)

# --- Energy Line Chart ---
def plot_total_energy_line(energy_df, dashboard_palette):
    corp = energy_df[(energy_df['Category'] == 'Corporate facilities energy use') & (energy_df['Metric'] == 'Total')]
    elec = corp[corp['Subcategory'] == 'Electricity'].groupby('year')['Value'].sum()
    fuel = corp[corp['Subcategory'] == 'Fuel'].groupby('year')['Value'].sum()
    total = elec.add(fuel, fill_value=0).reset_index(name='Total_Corp_Energy_MWh')
    if total.empty:
        return None
    fig, ax = plt.subplots(figsize=(10, 5.5))
    sns.lineplot(x='year', y='Total_Corp_Energy_MWh', data=total, ax=ax, color=dashboard_palette['accent_green_dark'], marker='o')
    format_dashboard_plot(fig, ax, 'Total Corporate Energy Consumption', ylabel_left='Energy (MWh)', axis_color_left=dashboard_palette['accent_green_dark'])
    plt.tight_layout()
    return fig_to_base64(fig)

# --- Fuel Mix Stacked Bar ---
def plot_fuel_mix_stacked(energy_df):
    fuels = ['Natural gas', 'Biogas', 'Gasoline', 'Diesel (other)', 'Diesel (mobile combustion)', 'Propane liquid']
    fuel_df = energy_df[(energy_df['Subcategory'] == 'Fuel') & (energy_df['Metric'].isin(fuels))]
    pivot = fuel_df.pivot_table(index='year', columns='Metric', values='Value', aggfunc='sum').fillna(0)
    if pivot.empty:
        return None
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot.plot(kind='bar', stacked=True, ax=ax, color=sns.color_palette('pastel'))
    format_dashboard_plot(fig, ax, 'Corporate Facilities Fuel Mix', ylabel_left='Energy (MWh)', axis_color_left='#6B7280')
    plt.tight_layout()
    return fig_to_base64(fig)
