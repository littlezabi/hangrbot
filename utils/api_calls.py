"""Make all external api calls from here"""

import requests
from utils.console import Console
import pprint


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

    def get_order_details(self, provider):
        """Get order external data"""
        url = provider.get("url")
        order_id = provider.get("id")
        api = provider.get("api")
        url = f"{url}{order_id}"

        headers = {
            "Content-Type": "application/json",
            "X-Api-Key": f"{api}",
        }
        response = requests.get(url, headers=headers)
        response = response.json()
        if response.get("error_code") == 0:
            return response
        Console(response, "error", "API.get_order_details")
        return None
