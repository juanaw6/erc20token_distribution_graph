import requests
from requests.auth import HTTPBasicAuth
import json
from concurrent.futures import ThreadPoolExecutor
from get_data import create_graph

# Function to handle request for each holder address
def fetch_transactions(holder_addr):
    global chainName, task_n, total_holders
    try :
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
    except :
        print(f"TASK {task_n}/{total_holders} FAIL: Get Tx from {holder_addr}")
        fetch_transactions(holder_addr)

task_n = 0
# Wallet address and API endpoint
chainName = "eth-mainnet"  # Ethereum Mainnet
tokenAddress = "0x0d8ca4b20b115D4DA5c13DC45Dd582A5de3e78BF"

url_token = f"https://api.covalenthq.com/v1/{chainName}/tokens/{tokenAddress}/token_holders_v2/?page-size=1000"

headers = {
    "accept": "application/json",
}
basic = HTTPBasicAuth('cqt_rQ97K7C4qyhXCX6rRc3Q4Pt93Vch', '')

response = requests.get(url_token, headers=headers, auth=basic)
response_json = response.json()

ticker_symbol = response_json['data']['items'][0]['contract_ticker_symbol']

holders = [holder['address'] for holder in response_json['data']['items']]
total_holders = len(holders)
print(f"TASK DONE: Get Holders of Token {ticker_symbol}")
print(f"TOTAL HOLDERS: {total_holders}")

with ThreadPoolExecutor(max_workers=8) as executor:
    data = list(executor.map(fetch_transactions, holders))

with open('result.json', 'w') as file:
    json.dump(data, file)

print("CREATING GRAPH")
create_graph()