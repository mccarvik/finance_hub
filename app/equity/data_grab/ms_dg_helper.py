from collections import defaultdict

# NOTES:
# 'Revenue' not included as its always 100
COL_MAP = {
    "Gross Margin %" : "grossMargin",                               # Margin
    "Operating Margin %" : "operatingMargin",                       # Margin
    "Dividends USD" : 'dividend',                                  # Gross
    "Revenue USD Mil" : 'revenue',                                  # Gross
    "COGS" : "cogs",                                                # Margin
    "SG&A" : "sg&a",                                                # Margin
    "R&D" : "r&d",                                                  # Margin
    "Other" : "other",                                              # Margin
    "Net Int Inc & Other" : "netIncomeIncOtherMargin",              # Margin
    "EBT Margin" : "EBTMargin",                                     # Margin
    "Operating Income USD Mil" : "operatingIncome",                 # Gross
    "Current Ratio" : "currentRatio",                               # Ratio
    "Quick Ratio" : "quickRatio",                                   # Ratio    
    "Financial Leverage" : "financialLeverage",                     # Ratio    
    "Debt/Equity" : "debtToEquity",                                 # Ratio    
    "Net Income USD Mil" : "netIncome",                             # Gross
    "Earnings Per Share USD" : "trailingEPS",                       # Gross
    "Payout Ratio % *" : "payoutRatio",                             # Ratio
    "Shares Mil" : "shares",                                        # Gross
    "Book Value Per Share * USD" : "bookValuePerShare",             # Per Share
    "Operating Cash Flow USD Mil" : "operatingCashFlow",            # Gross
    "Cap Spending USD Mil" : "capSpending",                         # Gross
    "Free Cash Flow USD Mil" : "freeCashFlow",                      # Gross
    "Free Cash Flow Per Share * USD" : "freeCashFlowPerShare",      # Per Share
    "Working Capital USD Mil" : "workingCapital",                   # Gross
    "Tax Rate %" : "taxRate",                                       # Ratio
    "Net Margin %" : "netIncomeMargin",                             # Margin
    "Asset Turnover (Average)" : "assetTurnoverRatio",              # Ratio
    "Return on Assets %" : "returnOnAssets",                        # Ratio
    "Return on Equity %" : "returnOnEquity",                        # Ratio
    "Return on Invested Capital %" : "returnOnCapital",             # Ratio
    "Interest Coverage" : "interestCoverage",                       # Ratio
    "Operating Cash Flow Growth % YOY" : "operatingCashFlowGrowth", # Ratio
    "Free Cash Flow Growth % YOY" : "freeCashFlowGrowth",           # Ratio
    "Cap Ex as a % of Sales" : "capExToSales",                      # Ratio
    "Free Cash Flow/Sales %" : "freeCashFlowToSales",               # Ratio
    "Free Cash Flow/Net Income" : "freeCashFLowToNetIncome",        # Ratio
    "Cash & Short-Term Investments" : "cashAndShortTermInv",        # Ratio
    "Accounts Receivable" : "accountsRecievable",                   # Ratio
    "Inventory" : "inventory",                                      # Ratio
    "Other Current Assets" : "otherCurrentAssets",                  # Ratio
    "Total Current Assets" : "totalCurrentAssets",                  # Ratio
    "Net PP&E" : "netPPE",                                          # Ratio
    "Intangibles" : "intangibles",                                  # Ratio
    "Other Long-Term Assets" : "otherLongTermAssets",               # Ratio
    "Accounts Payable" : "accountsPayable",                         # Ratio
    "Short-Term Debt" : "shortTermDebt",                            # Ratio
    "Taxes Payable" : "taxesPayable",                               # Ratio
    "Accrued Liabilities" : "accruedLiabilities",                   # Ratio
    "Other Short-Term Liabilities" : "otherShortTermLiabilities",   # Ratio
    "Total Current Liabilities" : "totalCurentLiabilities",         # Ratio
    "Long-Term Debt" : "longTermDebt",                              # Ratio
    "Other Long-Term Liabilities" : "otherLongTermLiabilities",     # Ratio
    "Total Liabilities" : "totalLiabilities",                       # Ratio
    "Total Stockholders' Equity" : "totalEquity",                   # Ratio
    "Days Sales Outstanding" : "daysSalesOutstanding",              # Gross
    "Days Inventory" : "daysInv",                                   # Gross
    "Payables Period" : "payablesPeriod",                           # Gross
    "Cash Conversion Cycle" : "cashConvCycle",                      # Gross
    "Receivables Turnover" : "recievablesTurnover",                 # Gross
    "Inventory Turnover" : "invTurnover",                           # Gross
    "Fixed Assets Turnover" : "fixedAssetsTurnover",                # Gross
}

CUSTOM_COL_MAP = {
    "Current Price" : "currentPrice",                               # Gross
    "Revenue Per Share" : "revenuePerShare",                        # Per Share
    "Total Cash Per Share" : "totalCashPerShare",                   # Per Share
    "Dividend Per Share" : "dividendPerShare",                      # Per Share
    "Dividend Yield" : "divYield",                                  # Ratio
    "Trailing PE" : "trailingPE",                                   # Ratio
    "Price to Book" : "priceToBook",                                # Ratio
    "Price to Sales" : "priceToSales",                              # Ratio
}



DAY_COUNTS = ["daysSalesOutstanding", "daysInv", "payablesPeriod", "cashConvCycle", 
            "recievablesTurnover", 'invTurnover', 'fixedAssetsTurnover']
BALANCE_SHEET = ["cashAndShortTermInv", "accountsRecievable", "inventory", "otherCurrentAssets",
                "totalCurrentAssets", "netPPE", "intangibles", "otherLongTermAssets", 
                "accountsPayable", "shortTermDebt", "taxesPayable", "accruedLiabilities",
                "otherShortTermLiabilities", "totalCurentLiabilities", "longTermDebt", 
                "otherLongTermLiabilities", "totalLiabilities", "totalEquity"
                "dividend", "revenue", "netIncome", "trailingEPS"]
INCOME_AND_CASH_FLOW = ["cogs", "sg&a", "r&d", "other", "operatingIncome", "operatingCashFlow",
                    "capSpending", "freeCashFlow", "workingCapital"]
PER_SHARE = ["bookValuePerShare", "freeCashFlowPerShare", "revenuePerShare", "totalCashPerShare",
            "dividendPerShare"]
RATIOS = ["currentRatio", "quickRatio", "financialLeverage", "debtToEquity", "assetTurnoverRatio",
        "interestCoverage", "capExToSales", "freeCashFlowToSales" "freeCashFLowToNetIncome",
        "trailingPE", "priceToBook", "priceToSales"]
MARGINS = ["grossMargin", "operatingMargin", "netIncomeIncOtherMargin", "EBTMargin",
            "netIncomeMargin"]
RETURNS = ["returnOnAssets", "returnOnEquity", "returnOnCapital"]
GROWTH = ["operatingCashFlowGrowth", "freeCashFlowGrowth"]
OTHER = ['shares', "payoutRatio", "taxRate"]

KEY_STATS = ['currentPrice', "divYield"]

# NOTES:
''' COLUMNS NOT USED:
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
'''
