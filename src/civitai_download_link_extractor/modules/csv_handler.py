import os
import csv
import pathlib

ROOT_DIR = pathlib.Path(__file__).parent.parent.parent.parent.resolve()


def is_csv(csv_path):
    return os.path.isfile(csv_path)


def read_csv(csv_path):
    model_set = set()
    with open(csv_path, "r", encoding="utf-8") as read_file:
        lines = read_file.readlines()

    if lines:
        for line in lines:
            model_set.add(line.split(",")[1])  # model_id

    return model_set, len(model_set)


def write_to_csv(data, csv_path):
    csv_name = csv_path.split("\\")[-1]
    csv_type = csv_name[:-4]

    model_set = set()
    model_count = 0
    models_in_csv = 0

    model_id, model_type, model_name, url = data

    if is_csv(csv_path):
        model_set, models_in_csv = read_csv(csv_path)
    else:
        pathlib.Path(csv_path).parents[0].mkdir(parents=True, exist_ok=True)

    with open(csv_path, "a+", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")

        if model_type == csv_type:
            if model_id not in model_set:
                writer.writerow([models_in_csv + 1, model_id, model_name, url])
                model_count += 1
                models_in_csv += 1

    return model_count
