from collections import defaultdict

COL_MAP = defaultdict(str, {
    "Gross Margin %" : "grossMargin",
    "Operating Margin %" : "operatingMargin",
    "Dividends USD" : 'dividends',
    "Revenue" : 'revenue',
    "COGS" : "cogs",
    "Gross Margin" : "grossMargin",
    "SG&A" : "sg&a",
    "R&D" : "r&d",
    "Other" : "other"
})