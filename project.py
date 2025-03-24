import requests, math, logging

logging.basicConfig(
    filename="basic.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def main():
    binance_api(url="https://api.binance.com/api/v3/ticker/price", params={"wrong" : "wrong"})

def binance_api(url : str, params : dict):
    if response := validate_http_response(requests.get(url=url, params=params)) != None:
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

if __name__ == "__main__":
    main()