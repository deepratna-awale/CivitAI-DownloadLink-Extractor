import json
import ast
import csv
import os
from os import getcwd, path, walk
import pathlib
from datetime import datetime
import glob
from collections import defaultdict

# Constants
CWD = pathlib.Path(__file__).parent.resolve()
ROOT_DIR = pathlib.Path().parent.resolve()
# relative path to all .civitai.info files, you don't need to seperate lora/locon/textualinversion/sd_model files.
# Copy all models info files to 'CivitAI_Info_Files' directory (folder).
INFO_FILES_PATH = ROOT_DIR+'/CivitAI_Info_Files/'
# Change CSV NAMES HERE IF NEEDED


def get_info_file_names(info_files_path):

    info_files = glob.glob(os.path.join(
        INFO_FILES_PATH, '**/*.info'), recursive=True)

    return info_files


def get_model_name(data):
    try:
        model_name = data['model']['name']
    except KeyError:
        return None
    return model_name


def get_model_type(data):
    try:
        model_type = data['model']['type']
    except KeyError:
        return None
    return model_type.lower()


def get_model_link(data):
    try:
        model_link = data['downloadUrl']
    except KeyError:
        return None
    return model_link


def is_csv(csv_path):
    return os.path.isfile(csv_path)


def read_csv(csv_path):
    model_set = set()
    with open(csv_path, 'r', encoding='utf-8') as read_file:
        lines = read_file.readlines()

    if lines:
        for line in lines:
            model_set.add(line.split(',')[1])

    return model_set, len(model_set)


def read_info_file(path):
    with open(path, 'r') as dataFile:
        try:
            data = json.load(dataFile)
            model_type = get_model_type(data)
            model_name = get_model_name(data)
            url = get_model_link(data)
        except json.decoder.JSONDecodeError:
            model_type = None
            model_name = None
            url = None
    return [model_type, model_name, url]


def write_to_csv(data, csv_path):
    csv_name = csv_path.split("/")[-1]
    csv_type = csv_name[:-4]

    model_set = set()
    model_count = 0
    models_in_csv = 0

    model_type, model_name, url = data[0:3]

    if is_csv(csv_path):
        model_set, models_in_csv = read_csv(csv_path)

    with open(csv_path, 'a+', newline='', encoding='utf-8') as csv_file:

        writer = csv.writer(csv_file, delimiter=',')

        if model_type == csv_type:
            if model_name not in model_set:
                writer.writerow([models_in_csv+1, model_name, url])
                model_count += 1
                models_in_csv += 1

    return model_count


if __name__ == "__main__":
    failed_files = []
    list_of_info_files = get_info_file_names(INFO_FILES_PATH)
    print("Found", len(list_of_info_files), "info files")

    model_count = defaultdict(int)

    for info_file in list_of_info_files:
        data = read_info_file(info_file)

        if None in data:
            failed_files.extend(info_file)
            continue
        model_type, model_name, url = data[:3]

        csv_name = model_type + '.csv'
        csv_path = ROOT_DIR + '/CSVs/' + csv_name

        write_to_csv(data, csv_path)

        print('Wrote', model_name, 'to', csv_name)
        model_count[model_type] += 1

    print("----------------------------\n\nWrote", str(dict(model_count)))
    if failed_files:
        now = datetime.now()
        current_time = now.strftime("%Y_%m_%d_%H_%M_%S")

        failed_files_txt_name = 'Failed_Files_' + current_time + '.txt'

        with open(failed_files_txt_name, 'w+') as txtfile:
            for file in failed_files:
                txtfile.write(file+'\n')

        print("Some files failed, details can be found in", os.getcwd()+failed_files_txt_name)
