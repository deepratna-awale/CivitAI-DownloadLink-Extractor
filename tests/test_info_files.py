import sys
import os
import pathlib
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from civitai_download_link_extractor import info_files


def main():
    path = pathlib.Path(
        r"CivitAI_Info_Files\realisticVisionV40_v40VAE.civitai.info"
    ).absolute()

    correct_id = "4201"
    correct_name = "realisticVisionV51_v40VAE".lower()
    correct_url = r"https://civitai.com/api/download/models/114367?type=Model&format=SafeTensor&size=full&fp=fp16"

    info_files.main()

    op_path = pathlib.Path(r"Output\checkpoint.csv").absolute()

    with open(op_path, "r") as csv:
        data = csv.readline()
        print(data)

    idx, model_id, model_name, url = data.split(",")

    print(model_id)
    print(model_name.lower())
    print(url)

    if (
        model_id == correct_id
        and model_name.lower() == correct_name
        and r"{}".format(url).strip() == correct_url
    ):
        print("Test Passed")
    else:
        print("Test Failed")


if __name__ == "__main__":
    main()
