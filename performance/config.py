import os
import datetime

today = datetime.datetime.today()
today = datetime.datetime(2023, 6, 19)
isExcel = True
if today.weekday() < 5:
    if isExcel:
        NAVFilename = "IBNAV_{0}.xlsx".format(today.strftime('%Y%m%d'))
    else:
        NAVFilename = "IBNAV_{0}.csv".format(today.strftime('%Y%m%d'))
else:
    raise Exception("No need to update performance since today is not weekday.")
# dateFormat = '%m/%d/%Y'
dateFormat = "%m/%d/%y"
basePath = 'C:/Dev/LifelongInvestorWebsite/lifelonginvestorllc.github.io/'
basePathReport = 'C:/Dev/LifelongInvestorWebsite/lifelonginvestorllc.github.io/reports/'
numericalColumns = ["Amount", "BM1Return", "Commodities", "Equities", "Fixed Income", "NAV"]
performanceColumns = ["Date", "Principal", "AUM", "Benchmark"]
performanceSaveFileName = "performance.csv"
reportCategory = {
    "Allocation by Asset Class": "Allocation by Asset Class",
    "Time Period Benchmark Comparison": "Time Period Benchmark Comparison",
    "Deposits And Withdrawals": "Deposits And Withdrawals"
}

columnName = {
    "Allocation by Asset Class": ["Date", "Commodities", "Equities", "Fixed Income", "NAV"],
    "Time Period Benchmark Comparison": ["Date", "BM1", "BM1Return"],
    "Deposits And Withdrawals": ["Date", "Type", "Amount"]
}
