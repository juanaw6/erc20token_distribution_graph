import requests
import json
import concurrent.futures
from API_KEY import *
from ratelimit import limits, sleep_and_retry

# Define the function to check if an address is a contract address
@sleep_and_retry
@limits(calls=5, period=1)  # Adjust the rate limit as needed
def check_contract_address(addr):
    api_url = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={addr}&apikey={ETHSCAN_APIKEY}"
    response = requests.get(api_url)
    data = response.json()
    if "result" in data and data["result"] and data["result"][0]['ContractName'] != '':
        return addr

# Load data from 'result.json'
with open('result.json', 'r') as file:
    data = json.load(file)

holders = []
for holder in data:
    if holder is not None:
        holders.append(holder['holder_addr'])

# Create a list to store contract addresses
list_contract = []

# Use ThreadPoolExecutor for parallel execution
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    # Submit API requests in parallel
    futures = [executor.submit(check_contract_address, addr) for addr in holders]

    # Collect results
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            list_contract.append(result)

# Print the contract addresses
for x in list_contract:
    print(x)
