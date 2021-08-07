import json
from keys import ACCESS_TOKEN
import urllib.parse
from urllib.request import Request, urlopen  # Python 3

import requests
import time

NOTION_URL = "https://api.notion.com/v1/pages"

def toDateFormat(from_date):
    conv=time.strptime(from_date, "%d/%m/%Y")
    return time.strftime("%Y-%m-%d", conv)


def toFloat(fromStr):
    print(fromStr)
    return float(fromStr.replace(',',''))


def insertRowIntoDb(row):

    payload = {
        "parent": {
            "database_id": "eae6f550b0ae409dbf18c89abc00e8ff"
        },
        "properties": {
            "Name": {
                "title": [{ "type": "text", "text": { "content": row[1] } }]
            },
            "Txn Date": {
                "type": "date",
                "date": { "start": toDateFormat(row[0]), "id": "txnDate" }
            },
            "Tnx Type": {
                "type": "select",
                "options": [{"name": "Debit", "id":"debit", "color": "green"}, {"name": "Credit", "id":"credit", "color": "red"}],
                        "select": { "name": "Credit" if row[2] == '0.00' else "Debit" }
            },
            "Amount": {
                "type": "number",
                "number": toFloat(row[2] if row[2] != '0.00' else row[3]),
                "format": "rupee"
            },
            "Category": {
                "type": "multi_select",
                                        "options": [{"name": "Personal", "id": "personal"}, { "name": "Transfers", "id": "transfers" }],
                "multi_select": []

            }
        }
    }


    # data = urllib.parse.urlencode(payload)
    # data = payload.encode('utf-8')
    data = str(payload).encode("utf-8")

    request = Request(NOTION_URL, data)
    request.add_header("Authorization", 'Bearer {}'.format(ACCESS_TOKEN))
    request.add_header("Content-Type", "application/json")
    request.add_header("Notion-Version", "2021-05-13")
    
    headers = {
        "Authorization": 'Bearer {}'.format(ACCESS_TOKEN),
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13"
    }


    r = requests.post(NOTION_URL, json=payload, headers= headers)

    print(request.get_method())
    
    # content = urlopen(request).read()

    

def getJsonData(validTransactions, closingBalance, fdBalance):

    transactions = []
    for row in validTransactions:
        transactions.append(getJsonDataFromPandaRow(row))

    jsonData = {
        "overview": {
            "closingBalance": closingBalance,
            "fdAmount": fdBalance
        },
        "transactions": transactions
    }
    return jsonData

def getJsonDataFromPandaRow(row):
    payload = {
        "Name": row[1],
        "txn_date": toDateFormat(row[0]),
        "Tnx Type": "Credit" if row[2] == '0.00' else "Debit",
        "Amount": toFloat(row[2] if row[2] != '0.00' else row[3]),
        "Category": "others"
    }
    return payload
