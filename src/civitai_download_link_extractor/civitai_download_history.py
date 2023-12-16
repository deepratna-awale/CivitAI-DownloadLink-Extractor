import pathlib
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import configparser
from termcolor import colored
import urllib3
import os
from collections import defaultdict
from datetime import datetime

from .modules import csv_handler as ch
from .modules import civitaihelper as civitai
from .modules import process_util as pu

PROCESS_NAME = "chrome.exe"
ARGS = "--remote-debugging-port=9222"

default_paths = {
    "WINDOWSx86": "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
    "WINDOWSx64": "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "LINUX": "google-chrome-stable",
    "MACOS": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
}


config = configparser.ConfigParser()
config.read("../config.ini")


target_url = "https://civitai.com/user/account/"
home_page_url = "https://civitai.com/"  # Replace with the actual home page URL
download_history = "https://civitai.com/user/downloads/"
login_url = "https://civitai.com/login?returnUrl=/"


class EmptyKeyException(Exception):
    pass


# Set up options to connect to the existing Chrome session
options = Options()
options.add_experimental_option("debuggerAddress", "localhost:9222")


def scroll_to_bottom():
    driver = webdriver.Chrome(options=options)
    elements_loaded_per_scroll = 20
    actions = ActionChains(driver)
    actions.move_to_element(downloads)

    actions.click().perform()
    body = driver.find_element(By.CSS_SELECTOR, "body")

    last_count = count = len(
        body.find_elements(By.CLASS_NAME, "mantine-Text-root.mantine-1wzmzwb")
    )

    no_of_page_down = 0

    while True:
        try:
            body.send_keys(Keys.PAGE_DOWN)
            no_of_page_down += 1
            # Wait to load page
            time.sleep(0.75)

            if no_of_page_down == 5:
                no_of_page_down = 0
                last_count = count

                if count < len(
                    body.find_elements(
                        By.CLASS_NAME, "mantine-Text-root.mantine-1wzmzwb"
                    )
                ):
                    count = len(
                        body.find_elements(
                            By.CLASS_NAME, "mantine-Text-root.mantine-1wzmzwb"
                        )
                    )

                if last_count >= count:
                    time.sleep(5)
                    count = len(
                        body.find_elements(
                            By.CLASS_NAME, "mantine-Text-root.mantine-1wzmzwb"
                        )
                    )
                    if last_count >= count:
                        return True

        except urllib3.exceptions.MaxRetryError:
            driver = webdriver.Chrome(options=options)
            body = driver.find_element(By.CSS_SELECTOR, "body")
            time.sleep(2)


def redirect_to_login():
    driver = webdriver.Chrome(options=options)
    # not loaded when user not logged in
    driver.maximize_window()
    driver.get(target_url)
    time.sleep(3)

    if driver.current_url == target_url:
        print("User is logged in.")
        driver.get(download_history)

    elif driver.current_url == home_page_url:
        print("Redirecting to Login Page")
        driver.get(login_url)

        element_to_wait_for = (By.CLASS_NAME, "tabler-icon.tabler-icon-bell")

        timeout = 180  # time in seconds to wait

        try:
            # Wait until the specified element is present
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(element_to_wait_for)
            )
            print("Login successful.")

        except TimeoutException as e:
            print(f"Timed out waiting for login to be successful.{e}")


def get_download_links():
    # Dict of Model_Name: url
    download_dict = defaultdict(list)

    driver = webdriver.Chrome(options=options)
    body = driver.find_element(By.CSS_SELECTOR, "body")

    time.sleep(1)
    print("Getting Page links from your download history.")

    href_elements = []
    name_elements = []

    href_elements.extend(
        body.find_elements(By.CLASS_NAME, "mantine-Text-root.mantine-1wzmzwb")
    )

    name_elements.extend(
        body.find_elements(By.CLASS_NAME, "mantine-Text-root.mantine-16hra2s")
    )

    print("Acquired", colored(len(href_elements), "cyan"), "page links.\n")
    print("Generating download urls via CivitAI Api.\n")

    print(f"{'Model':<100} | {'ID':^7} | {'TYPE':^10} | {'URL Exists':^7}")

    failed_links = []

    try:
        for name_element, href_element in zip(name_elements, href_elements):
            url = href_element.get_attribute("href")
            (
                model_id,
                version_id,
                model_info,
                model_type,
                model_list,
                model_name,
                downloadUrl,
            ) = None

            model_id = civitai.get_model_id(url)
            version_id = civitai.get_version_id(url)

            if version_id is None:
                model_info = civitai.get_model_info_from_id(model_id)
            else:
                model_info = civitai.get_model_info_from_version_id(version_id)

            if model_info:
                model_type = civitai.get_model_type(model_info)
                model_list = civitai.get_model_download_list(model_info)

                if model_list:
                    model_name = model_list[0].get("name", None)
                    downloadUrl = civitai.get_latest_model_download_link(model_list)

                if model_name is not None:
                    model_name = model_name.split(".")[0]

            if None in [model_id, downloadUrl]:
                failed_links.append(url)

            data = [model_id, model_type, model_name, downloadUrl]

            download_dict[model_id] = data

            print(
                f"{model_name.strip():<100} | {model_id.strip():^7} | {model_type.strip():^10} | {(downloadUrl != None):^7}"
            )

    except KeyboardInterrupt:
        print("Stopped by User.")

    driver.minimize_window()
    return download_dict, failed_links


def is_downloads():
    driver = webdriver.Chrome(options=options)
    driver.get(download_history)
    time.sleep(3)
    # Wait for the element with the specific class name to be present in the DOM
    stack = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                # this is the container containing the heading Downloads and the following download links
                By.CLASS_NAME,
                "mantine-Container-root.mantine-8fuc16",
            )
        )
    )

    # if 'no downloads' is found in stack text then raise exception
    if stack.text.lower().find("no downloads") != -1:
        print("No downloads found.")
        return None

    downloads = stack.find_element(By.CLASS_NAME, "mantine-Group-root.mantine-qhet0v")

    return downloads


def main():
    if not pu.process_exists(PROCESS_NAME):
        process_path = pu.default_launch(default_paths)

    if pu.process_exists(PROCESS_NAME):
        process_path = pu.get_path_from_process(PROCESS_NAME)
        pu.terminate_process(PROCESS_NAME)


    pu.open_process(process_path, ARGS)

    if pu.process_exists(PROCESS_NAME):
        print(
            f"Started {PROCESS_NAME.capitalize()} with args",
            colored({ARGS}, "green"),
        )


    time.sleep(1)
    print("-------------------------------------")
    print(colored("Waiting for Keyboard Interrupt.", "yellow"))
    print("Press", colored("Ctrl+C", "cyan"), "to terminate url collection!")

    try:
        redirect_to_login()

        downloads = is_downloads()

        try:
            if downloads is not None:
                scroll_to_bottom()

        except KeyboardInterrupt:
            print("Stopped by user. Please be patient.")
            time.sleep(1)

    finally:
        download_dict, failed_links = get_download_links()
        process_util.terminate_process("chrome.exe")
        model_set = ()
        model_count = defaultdict(int)

        print("Writing to Output.")

        for model_id in download_dict.keys():
            data = download_dict[model_id]
            model_id, model_type, model_name, downloadUrl = data

            csv_name = model_type + ".csv"
            csv_path = os.path.join(ch.ROOT_DIR, "Output", csv_name)

            ch.write_to_csv(data, csv_path)
            model_count[model_type] += 1

        print("----------------------------\nWrote", str(dict(model_count)))

        if failed_links:
            now = datetime.now()
            current_time = now.strftime("%Y_%m_%d_%H_%M_%S")

            failed_files_txt_name = "Failed_Links_" + current_time + ".txt"

            with open(failed_files_txt_name, "w+") as txtfile:
                for link in failed_links:
                    txtfile.write(link + "\n")

            print(
                "Some links failed, details can be found in",
                os.getcwd() + failed_files_txt_name,
            )

        print("---")
        print(colored("Done", "green"))

if __name__ == "__main__":
    main()