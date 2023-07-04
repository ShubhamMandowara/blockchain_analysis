import pandas as pd
import requests
from src.toml_helper import read_toml_file
import json


def get_data_from_alchemy(key, address):
    url = f"https://eth-mainnet.g.alchemy.com/v2/{key}"

    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "alchemy_getAssetTransfers",
        "params": [
            {
                "fromBlock": "0x0",
                "toBlock": "latest",
                "toAddress": f'{address}',
                "category": ["external"],
                "withMetadata": False,
                "excludeZeroValue": True,
                "maxCount": "0x3e8"
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.text


if __name__ == '__main__':
    settings = read_toml_file(path='../config/', file_name='settings.toml')
    transactions = get_data_from_alchemy(key=settings['KEY'], address='0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9')
    transactions = json.loads(transactions)['result']['transfers']
    df = pd.DataFrame(transactions)
    df.to_parquet('../data/0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9.parquet', index=False)
