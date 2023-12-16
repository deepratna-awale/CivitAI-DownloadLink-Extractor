# Credit to Qyabghuyn94 https://github.com/quanghuyn94/anything-model-batch-downloader/
import json
import os
import requests
import re


save_dict = [""]
extesion = [".safetensors", ".ckpt", ".pt"]


def find_values(key, json_obj, result_dict=None):
    try:
        if result_dict is None:
            result_dict = {}
        if isinstance(json_obj, dict):
            for k, v in json_obj.items():
                if k == key:
                    if k not in result_dict:
                        result_dict[k] = []
                    result_dict[k].append(v)
                else:
                    find_values(key, v, result_dict)
        elif isinstance(json_obj, list):
            for item in json_obj:
                find_values(key, item, result_dict)
        return result_dict
    except KeyError:
        return None


def get_model_id_from_info(model_info):
    model_id = None
    if model_info is not None:
        try:
            model_ids = find_values("modelId", model_info)
            model_id: str = model_ids["modelId"][0]
            return model_id
        except KeyError:
            return None
    return None


def get_model_id(url: str):
    regex_pattern = r"(\d+)"
    match = re.search(regex_pattern, url)
    if match:
        number = match.group()
        return number
    else:
        print("No id found in the URL")
        return None


def get_version_id(url: str):
    regex_pattern = r"modelVersionId=(\d+)"
    match = re.search(regex_pattern, url)
    model_version_id = match.group(1) if match else None

    return model_version_id


def get_model_info_from_id(model_id: str) -> dict:
    json_data = None
    if model_id is not None:
        model_id_api = "https://civitai.com/api/v1/models/"

        response = requests.get(f"{model_id_api}{model_id}")

        if response.status_code == 200:
            json_str = response.content.decode("utf-8")
            json_data = json.loads(json_str)

            return json_data
    return json_data


def get_model_info_from_version_id(model_id: str) -> dict:
    json_data = None
    if model_id is not None:
        versions_api = "https://civitai.com/api/v1/model-versions/"
        response = requests.get(f"{versions_api}{model_id}")

        if response.status_code == 200:
            json_str = response.content.decode("utf-8")
            json_data = json.loads(json_str)

            return json_data
    return json_data


def get_model_type(model_info: dict):
    model_type = None
    try:
        model_types = find_values("type", model_info)
        model_type: str = model_types["type"][0]
    except KeyError:
        return None

    return model_type.lower()


def get_model_download_list(model_info: dict):
    model_download_list = []

    if model_info is not None:
        try:
            file_infos = find_values("files", model_info)["files"]
            if file_infos:
                model_download_list = []
                for clean_file_info in file_infos:
                    if clean_file_info:
                        model_download_list.append(
                            {
                                "name": clean_file_info[0]["name"],
                                "type": clean_file_info[0]["type"],
                                "downloadUrl": clean_file_info[0]["downloadUrl"],
                            }
                        )
        except KeyError:
            return None

    return model_download_list


def get_latest_model_download_link(model_download_list: dict):
    latest_safetensors_link = None
    safetensors_links = []
    if model_download_list:
        safetensors_links = []
        latest_safetensors_link = ""

        for model in model_download_list:
            safetensors_links.append((model["downloadUrl"]))

    latest_safetensors_link = safetensors_links[0] if safetensors_links else None

    return latest_safetensors_link


# if __name__ == "__main__":
#     url = "https://civitai.com/models/103902/anything-v5-inpainting"

#     model_id = get_model_id(url)
#     ver_id = get_version_id(url)

#     print(model_id, ver_id)

#     model_info = get_model_info_from_id(model_id)
#     model_type = get_model_type(model_info)

#     model_list = get_model_download_list(model_info)

#     model = get_latest_model_download_link(model_list)
#     print(model)
