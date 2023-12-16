# CivitAI-DownloadLink-Extractor
 Extract _CivitAI Model Download Links_ via:
 - [x] Info Files
 - [x] Stable Diffusion Directory
 - [x] CivitAI Download History 


## Introduction
 - A handy tool to extract download links for CivitAI Models
 - Currently capable of extracting links for:
   - [x] LORAs
   - [x] Lycoris/ Locon
   - [x] Embeddings/ Textual Inversion
   - [x] Checkpoints
   - [ ] Poses (Untested)
   - [ ] VAEs (Untested)
   - [ ] Aesthetic Gradients (Untested)
   - [ ] Upscalers (Unimplemented)
   - [ ] Wildcards (Unimplemented)
  
  > Everything works with Civit AI download history!


# Requirements
1. Python v3.4 or higher
2. Pip installer
3. Chrome v120.x `(Other browsers wont work!)` - _only if you want to extract links your your CivitAI Download History._


# How to use
1. Make sure you have all files required.

```bash
D:\CivitAI-DownloadLink-Extractor
│   .gitattributes
│   .gitignore
│   config.ini
│   LICENSE
│   README.md
│   requirements.txt
│
├───CivitAI_Info_Files
│       _InfoFilesHere.txt
│
├───Output
│       _csv files go here.txt
│
└───src
    │   civitai_download_history.py
    │   info_files.py
    │   local_SD.py
    │
    └───modules
        │   civitaihelper.py
        │   csv_handler.py
        │   process_util.py
        └───
```

# Install Prerequisites

- Clone the repo
```bash
git clone https://github.com/deepratnaawale CivitAI-DownloadLink-Extractor.git
```

- Goto the Downloaded repo
  
```bash
cd CivitAI-DownloadLink-Extractor
```

- Make virtual enviorenment using pip `(recommended)`
```bash
python -m venv .venv
```

- Activate Virtual Enviorenment
```bash
.venv\Scripts\activate
```


- Install Requirements
```bash
pip install -r requirements.txt
```

- Run program!
```bash
python extract_links.py
```

## Method 1: Using Info Files
1. Copy all ".info" files to [**CivitAI_Info_Files**](./CivitAI_Info_Files) directory. You do not need to seperate the info files based on model type, CSVs will do that for you!


## Method 2: Stable Diffusion Path
> NOTE: ALL PATHS IN [`CONFIG.INI`](./config.ini) MUST BE ABSOLUTE PATHS

1. Edit `config.ini`.

```ini
[SD-DIR]
dir = <SD Folder Location>

[Output] # This is optional, Default is Project Directory/Output/
dir = <Custom Output Dir>
```

# Method 3: From CivitAI Download History
> You NEED Chrome(>=v120.x) for this. Once you start this option, DO NOT touch your keyboard or mouse.

`Please be patient!`

- You are required to be logged into CivitAI in chrome (the program will redirect you to login page if you arent.)

- The script will automatically try to launch chrome from default paths.
  - If path is not found then it will ask you to open chrome.
  - The program will get the path from the executable/ file for any OS.

- The browser will be closed and started in debug mode, so we can control it with program.
- Once the Debug Browser starts (You cant really tell it's in debug mode)
  - The script will automatically navigate to user account (to check if you are logged in).
  - If you are logged in it will navigate to your download history automatically.
  - It will scroll down to the bottom of the page (PLEASE DO NOT minimize, mouse click, or use the keyboard; the script WILL FAIL! Unfortunately, there is no particular way around this).


![Chrome Tutorial](https://github.com/deepratnaawale/CivitAI-DownloadLink-Extractor/blob/main/tutorial_gif.gif)

---
# CSV Structure
1. All your CSVs are with the following format:

Sr.no | Model ID| Model Name | Model URL
--- | --- | --- | ---
1 | 4201 | Realistic Vision V4.0 | https://civitai.com/api/download/models/114367
2 | ... | ... | ... 
3 | ... | ... | ... 

# Credits
* [Qyabghuyn94](https://github.com/quanghuyn94/) for civitai-helper.py: https://github.com/quanghuyn94/anything-model-batch-downloader/

## Author Notes [BONUS]
- I made this script to use with Runpod.
- If you are looking to **batch download** these extracted models to **Runpod**, goto my `Better Faster Stable Diffusion Runpod` repository. It uses multi threading to dramatically increase download speeds! You don't even need to wait for everything to download!
