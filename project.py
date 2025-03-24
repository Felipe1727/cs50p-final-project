import requests, math

def main():
    ...

def binance_api(url : str, params : dict):
    return validate_http_response(requests.get(url=url, params=params))
    

def validate_http_response(response : requests.models.Response):
    match response.status_code // 10 ** (int(math.log(response.status_code, 10))):
        case 4:
            print("User side error")
            return None
        case 5:
            print("Server side error")
            return None
        case _:
            return response

if __name__ == "__main__":
    main()