import requests, math

def main():
    ...

def binance_api(url : str, params : dict):
    if response := validate_http_response(requests.get(url=url, params=params)) != None:
        return check_error_codes(response= response)
    return response
    

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
        
def check_error_codes(response : requests.models.Response):
    r = response.json()
    if "code" in r:
        print(f"Error code {r["code"]}\n{r["msg"]}")
        return None

if __name__ == "__main__":
    main()