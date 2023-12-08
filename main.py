from API_KEY import *
import requests
from requests.auth import HTTPBasicAuth
import json
from concurrent.futures import ThreadPoolExecutor

from API_KEY import *
import requests
import json
from concurrent.futures import ThreadPoolExecutor
from ratelimit import limits, sleep_and_retry

# Define the rate limit (5 calls per second)
@sleep_and_retry
@limits(calls=5, period=1)
def fetch_transactions(holder_addr):
    global chainName, task_n, total_holders
    try:
        url_addr = f"https://api.covalenthq.com/v1/{chainName}/address/{holder_addr}/transactions_v3/"
        response = requests.get(url_addr, headers=headers, auth=basic)
        response_json = response.json()
        list_addr = {}
        for tx in response_json['data']['items']:
            address = tx['to_address']
            if address in holders and address != holder_addr:
                list_addr[address] = list_addr.get(address, 0) + 1
        task_n += 1
        print(f"TASK {task_n}/{total_holders} DONE: Get Tx from {holder_addr}")
        return {'holder_addr': holder_addr, 'recent_tx_freq': list_addr}
    except Exception as e:
        print(f"TASK {task_n}/{total_holders} FAIL: Get Tx from {holder_addr}")
        fetch_transactions(holder_addr)

# Rest of your code remains the same

chainName = "eth-mainnet"
url_token = f"https://api.covalenthq.com/v1/{chainName}/tokens/{TOKEN_ADDRESS}/token_holders_v2/?page-size=1000"
headers = {
    "accept": "application/json",
}
basic = HTTPBasicAuth(COVALENT_APIKEY, '')
response = requests.get(url_token, headers=headers, auth=basic)
response_json = response.json()

ticker_symbol = response_json['data']['items'][0]['contract_ticker_symbol']

holders = [holder['address'] for holder in response_json['data']['items']]
total_holders = len(holders)
print(f"TASK DONE: Get Holders of Token {ticker_symbol}")
print(f"TOTAL HOLDERS: {total_holders}")
task_n = 0
with ThreadPoolExecutor(max_workers=3) as executor:
    data = list(executor.map(fetch_transactions, holders))

with open('result.json', 'w') as file:
    json.dump(data, file)

print("Create the graph by running create_graph.py")