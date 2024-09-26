"""Make all external api calls from here"""

import requests
from utils.vars import API_KEY
from utils.console import Console


class API:
    """Request class to make api calls"""

    def __init__(self) -> None:
        pass

    def parse_request(self, data):
        """parse to get info from response"""
        data = data.get("data")
        external_id = data.get("external_id")
        provider = data.get("provider")
        return external_id, provider

    def get_order_details(self, order_id):
        """Get order external data"""
        url = f"https://usdsmm.com/adminapi/v2/orders/{order_id}"
        headers = {
            "Content-Type": "application/json",
            "X-Api-Key": f"{API_KEY}",
        }
        response = requests.get(url, headers=headers)
        response = response.json()
        if response.get("error_code") == 0:
            return response
        Console(response, "error", "API.get_order_details")
        return None
