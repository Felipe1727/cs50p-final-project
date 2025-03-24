import pytest, requests
from project import  check_error_codes


def test_binance_API():
    assert check_error_codes(requests.get(url="https://api.binance.com/api/v3/ticker")) == None
    assert check_error_codes(requests.get(url="https://api.binance.com/api/v3/ticker")) == None
    assert type(check_error_codes(requests.get(url="https://api.binance.com/api/v3/ticker/price"))) == requests.models.Response