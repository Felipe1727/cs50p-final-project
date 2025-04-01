import requests, math, logging, pandas as pd


def main():
    ...

def binance_api(endpoint : str, params = {}):
    response = validate_http_response(requests.get(url="https://api.binance.com/api/v3" + endpoint, params=params))
    if response != None:
        return check_error_codes(response= response)
    return response
    

def validate_http_response(response : requests.models.Response):
    match response.status_code // 10 ** (int(math.log(response.status_code, 10))):
        case 4:
            logging.error(f"User side error - HTTP {response.status_code}")
            return None
        case 5:
            logging.error(f"Server side error - HTTP {response.status_code}")
            return None
        case _:
            return response
        
def check_error_codes(response : requests.models.Response):
    r = response.json()
    if "code" in r:
        logging.error(f"Error code {r["code"]}: {r["msg"]}")
        return None
    return response

def trending():
    response = binance_api("/ticker/24hr")
    
    df = pd.DataFrame(response.json())
    
    columns_range = [
        "priceChange",
        "priceChangePercent",
        "weightedAvgPrice",
        "prevClosePrice",
        "lastPrice",
        "lastQty",
        "bidPrice",
        "bidQty",
        "askPrice",
        "askQty",
        "openPrice",
        "highPrice",
        "lowPrice",
        "volume",
        "quoteVolume"
    ]

    df = df[df["symbol"].str.endswith("USDC")]
    df[columns_range] = df[columns_range].astype(float)
    df = df.reset_index(drop=True)
    return df
        


if __name__ == "__main__":
    logging.basicConfig(
        filename="basic.log",
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    main()