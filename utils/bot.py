"""bot module"""

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from utils.console import Console
from utils.vars import (
    browser_path,
    profile_path,
    wait_after_page_load,
    check_for_new_messages_after,
    wait_to_load_chats,
)


class Bot:
    """Bot related methods is exsit here"""

    def __init__(self) -> None:
        options = Options()
        options.add_argument(f"--user-data-dir={profile_path}")
        options.add_experimental_option("detach", True)
        options.binary_location = browser_path
        self.driver = webdriver.Chrome(options=options)
        self.current_chats_tab = "all"

    def get_page(self, url):
        """
        get page based on url.
        """
        self.driver.get(url)
        Console(f"Wait {wait_after_page_load} seconds.")
        time.sleep(wait_after_page_load)

    def end_of_messages(self):
        """Go to end of the messages window"""
        try:
            button = self.driver.find_element(
                By.XPATH, '//*[@id="main"]/div[3]/div/div[1]/span/div'
            )
            button.click()
        except Exception as _:
            pass

    def get_recent_chats(self) -> list[str]:
        """Get Recent chats of the user."""
        try:
            self.end_of_messages()
            time.sleep(2)
            recent_chats = []
            try:
                # css = f"div._amk4._amkd._amk5 > div._amk6._amlo._amqa > div:nth-child({i}) > div > div.copyable-text"
                css = "div.copyable-text"
                reps = self.driver.find_elements(By.CSS_SELECTOR, css)
                for rep in reps:
                    recent_chats.append(rep.text)

            except Exception as e:
                print(e)

            return recent_chats

        except Exception as _:
            Console("Not chats found", "error")

        self.clear_search_bar()
        return []

    def confirm_responder_chat(self, provider: str):
        """
        Confirm that the provider chat is actually the real chat or not.
        its check the name of the provider to the title of the current chat.
        """
        title = self.driver.find_element(
            "#main > header > div._amie > div._amif > div > div > span"
        )
        if title.text == provider:
            return True
        return False

    # document.querySelector().innerText
    def send_response(self, message: str):
        """
        Send message to a person.
        Select the message input box and type the message
        """
        print("sending message to contact: ", message)
        try:
            time.sleep(2)
            message_box = self.driver.find_element(
                By.XPATH,
                '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p',
            )
            message_box.click()
            time.sleep(2)
            message_box.send_keys(message)
            time.sleep(1)
            message_box.send_keys(Keys.ENTER)
        except Exception as e:
            print(e)

    def switch_between_tabs(self, to="unread"):
        """switch to undread messages tab."""
        if self.current_chats_tab == to:
            return
        time.sleep(check_for_new_messages_after)
        try:
            xpath = '//*[@id="side"]/div[2]/button[2]'

            if to == "all":
                xpath = '//*[@id="side"]/div[2]/button[1]'
            button = self.driver.find_element(By.XPATH, xpath)
            time.sleep(2)
            button.click()

            if to == "unread":
                Console("checking unread messages.", "success")
            if to == "all":
                Console("swith to all messages tab.")

            time.sleep(2)

        except Exception as e:
            time.sleep(check_for_new_messages_after)
            Console(e, "error", "bot.swithToUnreadMsg")
            Console("Retrying", "alert", "bot.swithToUnreadMsg")
            self.switch_between_tabs(to)
        self.current_chats_tab = to

    def clear_search_bar(self):
        """Clear search bar input."""
        search_box = self.driver.find_element(
            By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'
        )
        try:
            search_box.click()
            time.sleep(1)
            try:
                clear = self.driver.find_element(
                    By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/span/button'
                )
                clear.click()
            except Exception as _:
                pass
            search_box.clear()
            time.sleep(1)
            return search_box

        except Exception as e:
            Console(e, "error", "Bot.clear_search_bar")
        return search_box

    def search_contact(self, contact: str) -> bool:
        """Search for the contact"""
        time.sleep(2)
        try:
            search_box = self.clear_search_bar()
            time.sleep(1)
            search_box.send_keys(contact)
            search_box.send_keys(Keys.ENTER)
            time.sleep(wait_to_load_chats)
            return True

        except Exception as _:
            Console(f"Can't find {contact} chats.", "error", "Bot.search_contact")
            return False

    def get_unread_chat_contacts(self):
        """Get contacts names of unread messages"""

        time.sleep(check_for_new_messages_after)
        try:
            unread_chats = self.driver.find_elements(
                By.CSS_SELECTOR,
                "#pane-side > div:nth-child(1) > div > div > div > div > div > div > div._ak8l > div._ak8o > div._ak8q > div > span",
            )  # Icon for new messages
            contact_names = []
            for chat in unread_chats:
                contact_name = chat.text
                contact_names.append(contact_name)

            return contact_names

        except NoSuchElementException:
            Console("No unread messages found.", "alert")
            return []


# if __name__ == '__main__':
#     bot = Bot()
#     bot.get_page('https://web.whatsapp.com')
#     print('user login status', bot.IsLoggedIn())
