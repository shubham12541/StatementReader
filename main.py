import json
from urllib import parse
from util import *
import tabula
import math
import datetime
import pandas as pd
import numpy as np
import urllib

from firebase import *


USERNAME = "shubham"


def mergeWithLastTransaction(lastRow, row):
    lastRow[1] = lastRow[1] + row[1]


def isValidDate(inputDate):
    isValidDate = True
    try :
        day,month,year = inputDate.split('/')
        datetime.datetime(int(year),int(month),int(day))
    except ValueError :
        isValidDate = False

    return isValidDate

def tansformToValidTransaction(row):
    validRow = []
    date = row[0][:10]

    validRow = pd.DataFrame.copy(row)

    if(len(row[0])>10 and isValidDate(date)):
        validRow[0] = date
        validRow[1] = row[0][11:]
    else:
        validRow[0] = np.nan
        validRow[1] = row[0]


    validRow[2] = row[2]
    validRow[3] = row[3]
    validRow[4] = np.nan
    validRow[5] = row[4]

    return validRow




# def categorizeTransactions(row):

# def convertToJsonData(validTransactions):


# TODO: call Notion API to insert
# TODO: organize the code 😅


filepath = "./statement_1.pdf"

# jsonData = tabula.read_pdf(filepath, output_format='json', pages='all')

tables = tabula.read_pdf(filepath, pages='all', silent=True,
                       pandas_options={
                           'header': None
                       })


HDFC_TXN_TABLE_INDEX = {
    "Txn Date": 0,
    "Narration": 1,
    "Withdrwals": 2,
    "Deposits": 3,
    "Closing Balance": 4
}

HDFC_SUMMARY_INDEX = {
    "Account Type": 1,
    "Balance": 2
}


TXN_CATEGORY = {
    0: "Investment", 
    1: "Transfers",
    2: "Online Shopping",
    3: "Food",
    4: "Video Games"
}

MAP_KEYWORD_TO_CATEGORY = {
    "groww": 0,
    "BSELim": 0,
    "chiragchaudhary": 1,
    "honey": 1,
    "playstation": 4,
    "amazon": 2
}


accountSummary = tables[0]
tnxCounter = 1
curTxnTable = tables[tnxCounter]

validTransaction = []

# Table 1: Summary
# Last Table: Interest
# Second last table: FD
# transaction table is merging with summary section 

for tnxCounter in range(1, len(tables) - 2):
    curTxnTable = tables[tnxCounter]
    isNanLookup = curTxnTable.isnull()

    # print(isNanLookup)

    for index, row in curTxnTable.iterrows():
        if(index == 0): 
            continue

        if(row[0] == "SUMMARY"):
            break

        if(len(row) == 5):
            row = tansformToValidTransaction(row)

        rowNanCount = row.isnull().sum()
        if(rowNanCount > 1):
            mergeWithLastTransaction(validTransaction[len(validTransaction) - 1], row)
        else:
            validTransaction.append(row)



# for row in validTransaction:
#     insertRowIntoDb(row)


closingBalance = 0.0
fdBalance = 0.0

for index, row in accountSummary.iterrows():
    if(row[0] != "INR"):
        continue

    if(row[HDFC_SUMMARY_INDEX["Account Type"]] == "SAVINGS ACCOUNTS"):
        closingBalance = row[2]
    elif(row[HDFC_SUMMARY_INDEX["Account Type"]] == "TERM DEPOSITS"):
        fdBalance = row[2]


print(closingBalance)
print(fdBalance)

jsonData = getJsonData(validTransaction, closingBalance, fdBalance)

saveUserdata(USERNAME, jsonData)

fo = open("output.raw", "w")
fo.write(str(validTransaction))
fo.close()


# tabula.convert_into("./statement_1.pdf", "output.csv", output_format="csv", pages='all')