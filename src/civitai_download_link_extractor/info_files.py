import json
import os
from os import getcwd, path, walk
import pathlib
from datetime import datetime
import glob
from collections import defaultdict
from .modules import csv_handler
from .modules import civitaihelper as civitai

# Constants
ROOT_DIR = pathlib.Path(__file__).parent.parent.parent.resolve()

# relative path to all .civitai.info files, you don't need to seperate lora/locon/textualinversion/sd_model/hypernetwork files.
# Copy all models info files to 'CivitAI_Info_Files' directory (folder).
INFO_FILES_PATH = os.path.join(ROOT_DIR, "CivitAI_Info_Files/")
# Change CSV NAMES HERE IF NEEDED


def get_info_file_names(info_files_path):
    info_files = glob.glob(os.path.join(INFO_FILES_PATH, "**/*.info"), recursive=True)

    return info_files


def read_info_file(path):
    with open(path, "r") as dataFile:
        model_info = (
            model_id
        ) = model_type = model_list = download_url = model_name = None
        try:
            model_info = json.load(dataFile)
            model_id = civitai.get_model_id_from_info(model_info)
            model_type = civitai.get_model_type(model_info)
            model_list = civitai.get_model_download_list(model_info)
            download_url = civitai.get_latest_model_download_link(model_list)

            if model_list is not None:
                model_name = model_list[0].get("name", None)
                if model_name is not None:
                    model_name = model_name.split(".")[0]
        except json.decoder.JSONDecodeError:
            model_id = None
            model_type = None
            model_name = None
            download_url = None

    return [model_id, model_type, model_name, download_url]


def main():
    failed_files = []
    list_of_info_files = get_info_file_names(INFO_FILES_PATH)
    print("Found", len(list_of_info_files), "info files")

    model_count = defaultdict(int)

    print(f"{'Model':<100} | {'ID':^7} | {'TYPE':^10} | {'URL Exists':^7}")

    for info_file in list_of_info_files:
        model_info = read_info_file(info_file)

        if None in model_info:
            failed_files.extend(info_file)
            continue

        model_id, model_type, model_name, download_url = model_info
        data = [str(model_id), model_type, model_name, download_url]

        csv_name = model_type + ".csv"
        csv_path = os.path.join(ROOT_DIR, "Output", csv_name)
        
        csv_handler.write_to_csv(data, csv_path)

        print(
            f"{model_name:<100} | {model_id:^7} | {model_type:^10} | {bool(download_url != None):^7}"
        )
        model_count[model_type] += 1

    print("----------------------------\n\nWrote", str(dict(model_count)))

    if failed_files:
        now = datetime.now()
        current_time = now.strftime("%Y_%m_%d_%H_%M_%S")

        failed_files_txt_name = "Failed_Files_" + current_time + ".txt"

        with open(failed_files_txt_name, "w+") as txtfile:
            for file in failed_files:
                txtfile.write(file + "\n")

        print(
            "Some files failed, details can be found in",
            os.getcwd() + failed_files_txt_name,
        )


if __name__ == "__main__":
    main()
