from collections import defaultdict

COL_MAP = {
    "Gross Margin %" : "grossMargin",
    "Operating Margin %" : "operatingMargin",
    "Dividends USD" : 'dividends',
    "Revenue USD Mil" : 'revenue',
    "COGS" : "cogs",
    "Gross Margin" : "grossMargin",
    "SG&A" : "sg&a",
    "R&D" : "r&d",
    "Other" : "other",
    "Operating Income USD Mil" : "operatingIncome",
    "Current Ratio" : "currentRatio",
    "Quick Ratio" : "quickRatio",
    "Financial Leverage" : "financialLeverage",
    "Debt/Equity" : "debtToEquity"
}
'''
Net Income USD Mil
Earnings Per Share USD
Payout Ratio % *
Shares Mil
Book Value Per Share * USD
Operating Cash Flow USD Mil
Cap Spending USD Mil
Free Cash Flow USD Mil
Free Cash Flow Per Share * USD
Working Capital USD Mil

Margins % of Sales
Revenue
COGS
Gross Margin
SG&A
R&D
Other
Operating Margin
Net Int Inc & Other
EBT Margin

Tax Rate %
Net Margin %
Asset Turnover (Average)
Return on Assets %
Financial Leverage (Average)
Return on Equity %
Return on Invested Capital %
Interest Coverage


Revenue %
Year over Year
3-Year Average
5-Year Average
10-Year Average
Operating Income %
Year over Year
3-Year Average
5-Year Average
10-Year Average
Net Income %
Year over Year
3-Year Average
5-Year Average
10-Year Average
EPS %
Year over Year
3-Year Average
5-Year Average
10-Year Average

Operating Cash Flow Growth % YOY
Free Cash Flow Growth % YOY
Cap Ex as a % of Sales
Free Cash Flow/Sales %
Free Cash Flow/Net Income

Cash & Short-Term Investments
Accounts Receivable
Inventory
Other Current Assets
Total Current Assets
Net PP&E
Intangibles
Other Long-Term Assets
Total Assets
Accounts Payable
Short-Term Debt
Taxes Payable
Accrued Liabilities
Other Short-Term Liabilities
Total Current Liabilities
Long-Term Debt
Other Long-Term Liabilities
Total Liabilities
Total Stockholders' Equity
Total Liabilities & Equity

Days Sales Outstanding
Days Inventory
Payables Period
Cash Conversion Cycle
Receivables Turnover
Inventory Turnover
Fixed Assets Turnover
Asset Turnover

'''