"""Initialize the app by executing this file"""

import time
from utils.bot import Bot
from utils.console import Console
from utils.messages import Messages
from utils.vars import wait_between_check_next_chat
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
            # if self.bot.search_contact(chat.get("provider")):
            if self.bot.search_contact("Meta AI"):
                self.bot.send_response(
                    f"""
                        external_id: {chat.get('external_id')} \n
                        order_id: {chat.get('order_id')} \n
                        type: {chat.get('type')}
                    """
                )
                self.replied.append(chat.get("provider"))
        print(self.replied)

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

    # def order_cancel(self, response):

    # def order_refil(self, response):
    #     """Handle refil request"""
    #     self.check_order_id(response)
    #     Console("Order refil request!", "alert")

    # def order_speed_up(self, response):
    #     """Handle speed up request"""
    #     self.check_order_id(response)
    #     Console("Order speed up request!", "alert")

    def type_and_request(self, response: str) -> dict:
        """
        Check the message type and call next request function
        like cancel order request function or speed up etc.
        """
        type_ = response.get("type")
        id_ = self.check_order_id(response)
        if id_ == "":
            self.bot.send_response("Please send your order id......")
        res_ = self.api.get_order_details(id_)
        if res_:
            external_id, provider = self.api.parse_request(res_)
            print(external_id, provider)
            return {"external_id": external_id, "provider": provider}
        Console(f"Order {type_} request!", "alert")
        return {}
        # if response.get("type") == "cancel":
        #     return self.order_cancel(response)

        # if response.get("type") == "speed-up":
        #     self.order_speed_up(response)

        # if response.get("type") == "refil":
        #     self.order_refil(response)

    def __repr__(self) -> str:
        return "Main class of HangrBot..."

    def __str__(self) -> str:
        return "Main class of HangrBot..."


if __name__ == "__main__":
    Hangr().start()
