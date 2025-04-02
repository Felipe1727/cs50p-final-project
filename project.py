import requests, math, logging, pandas as pd


def main():
    df = trending(replace_invalid=True)
    df.to_excel("df.xlsx")


def binance_api(endpoint : str, params = {}, headers = {}):
    response = validate_http_response(requests.get(url="https://api.binance.com/api/v3" + endpoint, params=params, headers=headers))
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

def trending(_symbol = "USDC", replace_invalid = False) -> pd.DataFrame:
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

    df = df[df["symbol"].str.endswith(_symbol)]
    df[columns_range] = df[columns_range].astype(float)
    df = df.reset_index(drop=True)
    if replace_invalid:
        df = replace(df)
    return df
        
def replace(df : pd.DataFrame):
    #TO-DO: Migrate the code in main into another function that works along with trending()
    invalid_usdc = (df[df['count'].astype(float) == 0].index[:])
    usdt_df = trending("USDT")
    invalid_usdc = df.loc[invalid_usdc]["symbol"].str.replace("USDC", "USDT")
    usdt_df = usdt_df[usdt_df["symbol"].isin(invalid_usdc)]
    #Eliminate the rows of the invalid_usdc_symbols that are not in usdt_df["symbol"]
    invalid_usdc = invalid_usdc[invalid_usdc.isin(usdt_df["symbol"])].sort_values()
    usdt_df = usdt_df.sort_values(by="symbol")
    usdt_df.index = invalid_usdc.index    

    for i in usdt_df.index:
        df.loc[i] = usdt_df.loc[i]

    df = df[df["count"] != 0]
    df.set_index("symbol", drop = True, inplace= True)
    return df


if __name__ == "__main__":
    logging.basicConfig(
        filename="basic.log",
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    main()