from django.db import models

# Year,Company,Fixed_Costs,Variable_Costs,Units_Sold,Sales_Revenue,Gross_Margin,Operating_Margin,Operating_Profit,Net_Profit,Equity,Liabilities,ROA,ROE,Current_Ratio,Debt_Ratio,Asset_Turnover

class FinancialData(models.Model):
    """
    Model to store financial data.
    """
    id = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length=10)
    year = models.IntegerField()  # Year of the financial data
    fixed_costs = models.FloatField(null=True, blank=True)  # Fixed costs
    variable_costs = models.FloatField(null=True, blank=True)  # Variable costs
    units_sold = models.IntegerField(null=True, blank=True)  # Units sold
    sales_revenue = models.FloatField(null=True, blank=True)  # Sales revenue
    gross_margin = models.FloatField(null=True, blank=True)  # Gross margin
    operating_margin = models.FloatField(null=True, blank=True)  # Operating margin
    operating_profit = models.FloatField(null=True, blank=True)  # Operating profit
    net_profit = models.FloatField(null=True, blank=True)  # Net profit
    equity = models.FloatField(null=True, blank=True)  # Equity
    liabilities = models.FloatField(null=True, blank=True)  # Liabilities
    roa = models.FloatField(null=True, blank=True)  # Return on Assets
    roe = models.FloatField(null=True, blank=True)  # Return on Equity
    current_ratio = models.FloatField(null=True, blank=True)  # Current ratio
    debt_ratio = models.FloatField(null=True, blank=True)  # Debt ratio
    asset_turnover = models.FloatField(null=True, blank=True)  # Asset turnover