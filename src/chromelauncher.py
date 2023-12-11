import psutil
import subprocess
import time
import pathlib
from pathlib import Path
from termcolor import colored


def process_exists(process_name):
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == process_name:
            return True
    return False

def findPath(name):
    for pid in psutil.pids():
        if psutil.Process(pid).name() == name:
            return psutil.Process(pid).exe()

while True:
    if process_exists('chrome.exe'):
        CHROME = findPath('chrome.exe')
        print('Found Chrome at:',CHROME)
        break
    else:
        input("Chrome is NOT Running. Please run Chrome and press <Enter> to begin.")
    

args = "--remote-debugging-port=9222"

time.sleep(2)
for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == 'chrome.exe':
        proc.kill()
try:
    print(colored("READ CAREFULLY", "red"))
    print(colored("After chrome opens, it will automatically open your CivitAI downloads page. Click on any blank region to start the process.", 'cyan'))
    print(colored("The script will automatically scroll your downloads page to the end of the page.", 'cyan'))
    print(colored("Let it.\nAfter the page is scrolled to the end, come back to terminal.", 'yellow'))
    input("Press Enter to Proceed.")

    result = subprocess.Popen([CHROME, args])

except subprocess.CalledProcessError as e:
    print(f"An error occurred: {e}")

if process_exists('chrome.exe'):
    print('Startin Chrome with debugging enabled', colored('@localhost:9222', 'green'))
