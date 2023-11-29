import os
import glob
import json
import csv
from CSVFromInfoFIles import *
import configparser
from datetime import datetime

config = configparser.ConfigParser()
config.read('config.ini')
# config.read('local-config.ini')


# Constants
CWD = os.getcwd()
SD_PATH = config['SD-DIR']['dir']
OP_PATH = config['Output']['dir']
if OP_PATH[0] == '<':
    OP_PATH = '/CSVs/'


def get_info_file_names_from_SD(models_dir):
    list_of_info_files = []
    info_files = glob.glob(os.path.join(
        models_dir, '**/*.info'), recursive=True)
    list_of_info_files.extend(info_files)
    return list_of_info_files


if __name__ == "__main__":
    failed_files = []
    models_dir = os.path.join(SD_PATH, 'models')
    embeddings_dir = os.path.join(SD_PATH, 'embeddings')
    
    list_of_info_files = get_info_file_names_from_SD(SD_PATH)
    print("Found", len(list_of_info_files), "info files")

    model_count = defaultdict(int)

    for info_file in list_of_info_files:
        data = read_info_file(info_file)
        
        if None in data:
            failed_files.append(info_file)
            continue
        
        model_type, model_name, url = data[:3]

        csv_name = model_type + '.csv'
        csv_path = CWD + OP_PATH + csv_name

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
    
