"""Initialize the app by executing this file"""

import time
from utils.bot import Bot
from utils.console import Console
from utils.messages import Messages
from utils.vars import wait_between_check_next_chat, providers, default_provider
from utils.api_calls import API


class Hangr:
    """Main class of HangrBot..."""

    def __init__(self) -> None:
        self.messages = Messages()
        self.bot = Bot()
        self.bot.get_page("https://web.whatsapp.com")
        self.api = API()
        self.replied = []
        self.pendings = []

    def iter_contacts(self, contacts):
        """Iterate through contacts"""
        iter_ = 0
        for chats in contacts:
            self.bot.clear_search_bar()
            if chats in self.replied:
                continue
            time.sleep(1)
            if self.bot.search_contact(chats):
                msgs = self.bot.get_recent_chats()
                if len(msgs) > 0:
                    get_last_msg = [msgs[-1]]
                    response = self.messages.compare_messages(get_last_msg)
                    last_msg = response.get(get_last_msg[0])
                    if last_msg:
                        res_ = self.type_and_request(last_msg)
                        if not res_.get("external_id"):
                            Console(
                                f"Failed to get external id from api request: {last_msg}. "
                            )
                            continue
                        self.bot.send_response(last_msg.get("response"))
                        self.replied.append(chats)
                        self.pendings.append(
                            {
                                "contact": chats,
                                "external_id": res_.get("external_id"),
                                "provider": res_.get("provider"),
                                "message": get_last_msg,
                                **last_msg,
                            }
                        )
                        # {"external_id": external_id, "provider": provider}
                else:
                    Console("There is no chats found!", "alert", "App.start")
            contacts.pop(iter_)
            iter_ += 1
            time.sleep(wait_between_check_next_chat)

    def send_to_provider(self):
        """Send message to provider"""
        self.bot.switch_between_tabs("all")
        for chat in self.pendings:
            if chat.get("provider") in self.replied:
                continue
            self.bot.clear_search_bar()

            prv = chat.get("provider")
            if not self.bot.confirm_responder_chat(chat.get("contact")):
                Console(
                    f"Provider is not confirmed to send message. sending message to default provider ({default_provider})",
                    "Error",
                    "Api.send_response",
                )
                prv = default_provider

            if self.bot.search_contact(prv):
                self.bot.send_response(
                    f"""
                        {chat.get('external_id')} - {chat.get('type')}
                    """,
                )
                self.replied.append(chat.get("provider"))

    def start(self):
        """Start the bot by calling this method"""
        self.bot.switch_between_tabs()

        while True:
            self.replied = []
            self.pendings = []
            # self.pendings = []
            self.bot.switch_between_tabs("unread")
            contacts = self.bot.get_unread_chat_contacts()
            self.bot.clear_search_bar()
            if len(contacts) == 0:
                print("No new messages.")
            self.iter_contacts(contacts)

            if len(self.pendings) > 0:
                self.send_to_provider()

    def check_order_id(self, response) -> str:
        """
        Check order id in response if its exist
        then move forward otherwise return missing id message
        """
        if response.get("order_id"):
            return response.get("order_id")
        Console("order id is not exist", "alert", "message.check_order_id")
        return ""

    def get_provider(self, customer_id):
        """
        Finds the site configuration based on the provided customer ID.

        This function iterates through a dictionary of site configurations,
        where each site has an associated customer ID range. If the `customer_id`
        falls within the specified range of any site, the corresponding site details
        are returned.

        Args:
            data (dict): A dictionary where the key is the site name (string), and
                        the value is a dictionary with a `range` (list of two integers)
                        and a `url` (string).
            customer_id (int): The customer ID to check against the site ranges.

        Returns:
            (dict or None): Returns a dictionary containing the matched site and its details
                        if the customer ID falls within one of the ranges. Returns `None`
                        if no match is found.

        Example:
            x = {
                "usdsmm.com": {
                    "range": [100000, 500000],
                    "url": "https://usdsmm.com/adminapi/v2/orders/"
                },
                "cashsmm.com": {
                    "range": [500000, 1000000],
                    "url": "https://usdsmm.com/adminapi/v2/orders/"
                },
                "prixsmm.com": {
                    "range": [3300000, 100000000],
                    "url": "https://usdsmm.com/adminapi/v2/orders/"
                }
            }

            result = get_matching_site(x, 550000)
            print(result)
            # Output: {'cashsmm.com': {'range': [500000, 1000000], 'url': 'https://usdsmm.com/adminapi/v2/orders/'}}
        """
        if customer_id == "":
            return None
        for site, details in providers.items():
            lower, upper = details["range"]
            print(customer_id, type(customer_id), f"{customer_id}")
            if lower <= int(customer_id) <= upper:
                return {"provider": site, "url": details["url"], "api": details["API"]}
        return None

    def type_and_request(self, response: str) -> dict:
        """
        Check the message type and call next request function
        like cancel order request function or speed up etc.
        """
        type_ = response.get("type")
        id_ = self.check_order_id(response)
        if id_ == "":
            self.bot.send_response("Please send your order id......")
        provider = self.get_provider(id_)
        if not provider:
            Console(
                "Range is not matched with customer id.",
                "error",
                "Hangr.type_and_request",
            )
            return {}
        res_ = self.api.get_order_details({**provider, "id": id_})
        if res_:
            external_id, provider = self.api.parse_request(res_)
            return {"external_id": external_id, "provider": provider}
        Console(f"Order {type_} request!", "alert")
        return {}

    def __repr__(self) -> str:
        return "Main class of HangrBot..."

    def __str__(self) -> str:
        return "Main class of HangrBot..."


if __name__ == "__main__":
    Hangr().start()
