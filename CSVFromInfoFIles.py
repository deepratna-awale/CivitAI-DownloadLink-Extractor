import json

import csv

import os

from os import getcwd, path, walk

import glob

# Constants
CWD = os.getcwd()
# relative path to all .civitai.info files, you don't need to seperate lora/locon/textualinversion/sd_model files.
# Copy all models info files to 'CivitAI_Info_Files' directory (folder).
INFO_FILES_PATH = CWD+'/CivitAI_Info_Files/'
# Change CSV NAMES HERE IF NEEDED


CSV_NAMES = {
    'lora': 'CSVs/LORAs.csv',
    'locon': 'CSVs/LORAs.csv',
    'textualinversion': 'CSVs/TextualInversions.csv',
    'checkpoint': 'CSVs/ckpts.csv'
}


def get_info_file_names(info_files_path):
    list_of_info_files = []
    
    info_files = glob.glob(os.path.join(info_files_path,'*.info'))
    json_files = glob.glob(os.path.join(info_files_path, '*.json'))

    list_of_info_files.extend(info_files+json_files)
    
    return list_of_info_files


def rename_to_json(list_of_file_names):

    files_renamed = []

    for file_name in (list_of_file_names):
        if '.info' in file_name:
            fullpath = os.path.join(INFO_FILES_PATH, file_name)
            os.rename(fullpath, fullpath[:-5]+'.json')
            files_renamed.append(fullpath)

    return files_renamed


def get_model_name(data):

    model_name = data['model']['name']

    return model_name


def get_model_type(data):

    model_type = data['model']['type']

    return model_type.lower()


def get_model_link(data):

    model_link = data['downloadUrl']

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
        data = json.load(dataFile)

    model_type = get_model_type(data)
    model_name = get_model_name(data)
    url = get_model_link(data)
    
    return model_type, model_name, url



def write_csv(csv_type='lora'):
    
    model_set = set()
    model_count = 0
    models_in_csv = 0

    csv_name = CSV_NAMES[csv_type]
    csv_path = os.path.join(CWD, csv_name)
    list_of_info_files = get_info_file_names(INFO_FILES_PATH)


    if is_csv(csv_path):
        model_set, models_in_csv = read_csv(csv_path)
        print('CSV file', csv_name, 'already exists with', models_in_csv, csv_type)
    else:
        print('Created file', os.path.join(CWD, csv_name))
    
    with open(csv_path, 'a+', newline='', encoding='utf-8') as csv_file:
        
        writer = csv.writer(csv_file, delimiter=',')

        for file_name in list_of_info_files:
            info_file_path = os.path.join(INFO_FILES_PATH, file_name)
            model_type, model_name, url = read_info_file(info_file_path)
            
            if model_type == csv_type:
                if model_name not in model_set:
                    writer.writerow([models_in_csv+1, model_name, url])
                    model_count += 1
                    models_in_csv += 1

    return model_count


if __name__ == "__main__":

    list_of_info_files = get_info_file_names(INFO_FILES_PATH)
    print("Found", len(list_of_info_files), "info files")

    files_renamed = rename_to_json(list_of_info_files)
    print('Renamed', len(files_renamed), 'file(s).')

    for csv_type in CSV_NAMES.keys():
        model_count = write_csv(csv_type)
        print('Wrote', model_count, 'new', csv_type, 'links to', CSV_NAMES[csv_type])
