"""HangrBot all constants and configuration variables"""

import os
import json
from utils.console import Console

assert os.path.isfile("./config.json")
with open("./config.json", "r", encoding="utf-8") as f:
    config = json.load(f)
    wait_after_page_load = config["TIMES"]["wait_after_page_load"]
    wait_to_load_chats = config["TIMES"]["wait_to_load_chats"]
    wait_normal_switch_after = config["TIMES"]["wait_normal_switch_after"]
    check_for_new_messages_after = config["TIMES"]["check_for_new_messages_after"]
    wait_between_check_next_chat = config["TIMES"]["wait_between_check_next_chat"]
    API_KEY = config["api_key"]
    driver_path = config["PATHS"]["driver_path"]
    profile_path = config["PATHS"]["profile_path"]
    browser_path = config["PATHS"]["browser_path"]
    responses_file = config["PATHS"]["responses_file"]


def check_profile():
    """Check HangrBot profile folder if not exist then create new"""
    exist = os.path.isdir(profile_path)
    if not exist:
        try:
            os.mkdir(profile_path)

        except Exception as e:
            Console(
                f"Error on creating profile directory on {profile_path}. Error is {e}",
                "error",
                "Vars.check_profile",
            )


def check_browser():
    """Check browser is in path or not"""
    exist = os.path.isfile(browser_path)
    if not exist:
        Console(
            f"Browser is not in path. please check this path {browser_path}.",
            "error",
            "Vars.check_browser",
        )


check_browser()
check_profile()
