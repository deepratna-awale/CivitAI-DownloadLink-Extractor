import os
import glob
import json
import csv
from collections import defaultdict
import configparser
from datetime import datetime
import pathlib
from pathlib import Path
from termcolor import colored

from .info_files import read_info_file
from .modules import csv_handler
from .modules import civitaihelper as civitai

config = configparser.ConfigParser()

# config.read('config.ini')
ROOT_DIR = pathlib.Path(__file__).parent.parent.parent.resolve()

config_name = "config.ini"
config_path = Path(ROOT_DIR, config_name)

print(config_path)
config.read(config_path)

def get_paths_from_config():
# Constants
    OP_PATH, SD_PATH = 'Output', None
    try:
        SD_PATH = config["SD-DIR"]["dir"]
        
        if SD_PATH[0] == "<":
            print(
                "Couldn't find",
                colored("Stable Diffusion Directory", "red"),
                "make sure it is present in",
                colored("config.ini", "cyan"),
                "under SD-DIR")
            exit()
    
    except KeyError:
        print("Key not found.")

    try:
        OP_PATH = config["Output"]["dir"]
        if OP_PATH[0] == "<":
            OP_PATH = "Output"
    except KeyError:
        print(f"Key not found.")
    
    return OP_PATH, SD_PATH


def get_info_file_names_from_SD(models_dir):
    list_of_info_files = []
    info_files = glob.glob(os.path.join(models_dir, "**/*.info"), recursive=True)
    list_of_info_files.extend(info_files)
    return list_of_info_files


def main():
    OP_PATH, SD_PATH = get_paths_from_config()
    failed_files = []

    models_dir = os.path.join(SD_PATH, "models")
    embeddings_dir = os.path.join(SD_PATH, "embeddings")

    list_of_info_files = get_info_file_names_from_SD(SD_PATH)
    print("Found", len(list_of_info_files), "info files")

    model_count = defaultdict(int)

    print(f"{'Model':<100} | {'ID':^7} | {'TYPE':^10} | {'URL Exists':^7}")

    for info_file in list_of_info_files:
        try:
            model_info = read_info_file(info_file)
            model_id, model_type, model_name, downloadUrl = model_info

            csv_name = model_type + ".csv"
            csv_path = os.path.join(ROOT_DIR, OP_PATH, csv_name)

            csv_handler.write_to_csv(model_info, csv_path)

            print(
                f"{model_name.strip():<100} | {str(model_id).strip():^7} | {model_type.strip():^10} | {(downloadUrl != None):^7}"
            )

            # print('Wrote', model_name, 'to', csv_name)
            model_count[model_type] += 1
        except (KeyError, IndexError, Exception) as e:
            print(f"Recieved Exception/Error {e}")

    print(
        "----------------------------\n\nWrote",
        colored(str(dict(model_count)), "cyan"),
        "\n",
    )

    if failed_files:
        now = datetime.now()
        current_time = now.strftime("%Y_%m_%d_%H_%M_%S")

        failed_files_txt_name = "\\Failed_Files_" + current_time + ".txt"

        with open(failed_files_txt_name, "w+") as txtfile:
            for file in failed_files:
                txtfile.write(file + "\n")

        print(
            colored("Some files failed, details can be found in", "red"),
            os.getcwd() + failed_files_txt_name,
        )


if __name__ == "__main__":
    main()