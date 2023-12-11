import chromelauncher
import os
import pathlib
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import csv
import configparser
from termcolor import colored

config = configparser.ConfigParser()
config.read('../config.ini')

CWD = pathlib.Path(__file__).parent.parent.resolve()


class EmptyKeyException(Exception):
    pass

try:
    path_in_config = config['CivitAI-Downloads-History']['path']
    if path_in_config[0] == '<':
        raise EmptyKeyException
    else:
        PATH = Path(path_in_config)

except KeyError:
    print(colored("Couldn't find key. Falling back to default windows chrome path.", "yellow"))
    PATH = Path(CWD, "CSVs/user-downloads.csv")

except EmptyKeyException:
    print(colored('The chrome path in config.ini is empty. Falling back to default windows path.', 'yellow'))
    PATH = Path(CWD,"CSVs/user-downloads.csv")


class LoginRequired(Exception):
    pass


SITE = "https://civitai.com/user/downloads"

interrupted = False

# Set up options to connect to the existing Chrome session
options = Options()
options.add_experimental_option("debuggerAddress", "localhost:9222")

# Connect to the existing Chrome session
driver = webdriver.Chrome(options=options)

# Dict of Model_Name: url
download_dict = dict()

def write_to_csv(path, download_dict):

    with open(path, 'w+',  newline='', encoding='utf-8') as csv_file:
    
        writer = csv.writer(csv_file, delimiter=',')
        
        count = 0
        
        for key in download_dict.keys():
            
            writer.writerow([key.strip(), download_dict[key]])
            count += 1
        
        print('Wrote', colored(str(count), 'cyan'), 'unique download links.')


if __name__ == "__main__":
    print("\n\n\n---")
    print(colored('Waiting for Keyboard Interrupt.', 'yellow'))
    print('Press', colored('Ctrl+C', 'cyan'), 'when you have reached bottom of your downloads page. DO NOT SPAM IT, THE PROGRAM WILL TERMINATE!')
    
    try:
        # Navigate to the desired URL
        driver.get(SITE)
        body = driver.find_element(By.CSS_SELECTOR, 'body')

        # Wait for the element with the specific class name to be present in the DOM
        stack = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.CLASS_NAME, "mantine-Stack-root.mantine-fui8ih" # this is the container containing the heading Downloads and the following download links
        )))

        if stack.text.lower().find('no downloads') != -1: # if 'no downloads' is found in stack text then raise exception
            raise LoginRequired
        
        try:
            while True:
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.5)

        except KeyboardInterrupt:
            print('Stopped by user. Please be patient.')
            interrupted = True
            time.sleep(2)
                
    except LoginRequired as e:
        print(colored('Following exception was recieved', 'yellow'), e)
        print('Maybe you are not logged in?')
        print(colored('Log into CivitAI and restart the script.', 'red')) 
        print(colored('If you are logged into CivitAI already (IN CHROME) restart the script.', 'yellow'))


    finally:
        driver = webdriver.Chrome(options=options)
        body = driver.find_element(By.CSS_SELECTOR, 'body')
        print("Getting URLs.")

        

        href_elements = []
        name_elements = []
        
        href_elements.extend(body.find_elements(
            By.CLASS_NAME, "mantine-Text-root.mantine-1wzmzwb"))
        
        name_elements.extend(body.find_elements(
        By.CLASS_NAME, "mantine-Text-root.mantine-16hra2s"))

        print('Acquired', len(href_elements), 'urls.')

        for name_element, href_element in zip(name_elements, href_elements):
            
            name = name_element.text
            href = href_element.get_attribute('href')
            
            if name not in download_dict:
                download_dict[name] =  href
        
        PATH.parent.mkdir(exist_ok=True, parents=True)
        write_to_csv(PATH, download_dict)
        
        driver.quit()
        
        print("---")
        print(colored("Done", 'green'))
