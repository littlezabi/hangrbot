"""
     Check Messages and its possibles reply
"""

import json
import re
from utils.vars import responses_file
from utils.console import Console


class Messages:
    """
    Check Messages and its possibles reply
    """

    def __init__(self) -> None:
        self.responses = []
        self.get_responses()

    def extract_id(self, text: str) -> str:
        """Extract order id from message"""
        match = re.search(r"^\d+", text)
        if match:
            return match.group()
        Console("Order id not found in message", "alert", "Messages.extract_id")
        return ""

    def compare_messages(self, messages: list[str]) -> dict:
        """Compare messages and find its possible replys"""
        response = {}
        for message in messages:
            for res in self.responses.keys():
                if res.lower() in message.lower():
                    response[message] = {
                        "response": self.responses[res][0],
                        "type": self.responses[res][1],
                        "order_id": self.extract_id(message),
                    }
                    break
        return response

    def get_responses(self):
        """get all responses from file"""
        with open(responses_file, "r", encoding="utf-8") as f:
            self.responses = json.load(f)
