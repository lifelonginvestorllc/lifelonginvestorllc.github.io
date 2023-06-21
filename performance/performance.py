from typing import List

import pandas as pd
import csv
import os
import numpy as np
import datetime as dt
from pandas_datareader import data as pdr
import config


# import yfinance as yf
# yf.pdr_override()


class Performance:
    def __init__(self):
        self.IBRawData = None
        self.NAVData = None
        self.benchmarkData = None
        self.depositAndWithdrawData = None
        self.mergedReportData = None
        self.performanceData = None
        self.basePath = config.basePath

    def readIBReport(self, isExcel=True):
        if isExcel:
            self.IBRawData = pd.read_excel(config.basePathReport + config.NAVFilename, skiprows=2, header=None)
        else:
            self.IBRawData = pd.read_csv(config.basePathReport + config.NAVFilename, skiprows=2, header=None, skip_blank_lines=True)
        self.NAVData = self.filterIBReport(self.IBRawData, config.reportCategory["Allocation by Asset Class"])
        self.benchmarkData = self.filterIBReport(self.IBRawData, config.reportCategory["Time Period Benchmark Comparison"])
        self.depositAndWithdrawData = self.filterIBReport(self.IBRawData, config.reportCategory["Deposits And Withdrawals"])
        self.mergedReportData = self.mergeDataByColumn(self.NAVData, self.benchmarkData, self.depositAndWithdrawData)
        self.computePerformance()

    def filterIBReport(self, df: pd.DataFrame, reportCategory: str):
        # Use first column to filter the report category (e.g., NAV, etc). Set the header and set Date as index for merging purpose.
        tempDF = df[df.iloc[:, 0] == reportCategory].iloc[1:, :]
        filteredDF = tempDF.rename(columns=tempDF.iloc[0]).drop(tempDF.index[0]).dropna(axis=1)[config.columnName[reportCategory]]
        if "Date" not in filteredDF.columns:
            raise Exception("Date has to be in the header of the dataframe")
        if reportCategory == "Allocation by Asset Class":
            filteredDF["Date"] = pd.to_datetime(filteredDF["Date"], format='%Y%m%d')
            filteredDF["Date"] = pd.to_datetime(filteredDF["Date"]).dt.strftime(config.dateFormat)
        else:
            filteredDF["Date"] = pd.to_datetime(filteredDF["Date"]).dt.strftime(config.dateFormat)

        filteredDF.set_index("Date", inplace=True)
        if reportCategory == "Deposits And Withdrawals":
            return self.processDepositReport(filteredDF)
        return filteredDF

    def mergeDataByColumn(self, *dfs, join="outer", setNumericCol=True):
        dfs = list(dfs)
        for i in range(1, len(dfs)):
            dfs[i] = dfs[i].merge(dfs[i - 1], how=join, left_index=True, right_index=True).fillna(0)
        if setNumericCol:
            result = dfs[-1][config.numericalColumns].apply(pd.to_numeric)
        else:
            result = dfs[-1]
        self.mergedReportData = result
        return self.mergedReportData

    def computePerformance(self, startingDate="04/03/2023", save=True):
        if len(self.mergedReportData) == 0:
            raise Exception("The merged report data is not ready yet.")

        df = self.mergedReportData.copy(deep=True).reset_index()
        df['Benchmark'] = df['Amount']
        for i in range(1, len(df)):
            df.loc[i, 'Benchmark'] = df.loc[i - 1, 'Benchmark'] * (df.loc[i - 1, 'BM1Return'] / 100 + 1) + df.loc[i, 'Amount']
        df['Benchmark'] = (df['Benchmark'] / 10000).round(decimals=2)
        df['Principal'] = (df['Amount'].cumsum() / 10000).round(decimals=2)
        df['AUM'] = (df['NAV'] / 10000).round(decimals=2)

        df = df[config.performanceColumns][df["Date"] >= startingDate]
        df['Date'] = pd.to_datetime(df['Date'])
        # df["Date"] = df['Date'].dt.month.astype(str) + '/' + df['Date'].dt.day.astype(str) + '/' + df['Date'].dt.strftime('%y')
        df["Date"] = df['Date'].dt.strftime('%m/%d/%y')

        if save:
            df.to_csv(config.basePath + config.performanceSaveFileName, index=False)
        return df

    def processDepositReport(self, df: pd.DataFrame):
        df['Amount'] = df['Amount'].apply(pd.to_numeric)
        res = df.groupby('Date').agg({"Type": "first", "Amount": sum})
        return res

    def fix_csv_file(self, file_path):
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            lines = list(reader)

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.fix_lines(lines))

    def fix_lines(self, lines):
        fixed_lines = []
        for line in lines:
            if line and not line[-1].endswith(','):
                line[-1] += ','
            fixed_lines.append(line)
        return fixed_lines


if __name__ == '__main__':
    report = Performance()
    report.readIBReport()  # read and compute performance
