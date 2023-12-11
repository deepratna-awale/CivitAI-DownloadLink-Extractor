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
   - [ ] Poses (Unimplemented)
   - [ ] VAEs (Untested)
   - [ ] Aesthetic Gradients (Untested)
   - [ ] Upscalers (Unimplemented)
   - [ ] Wildcards (Unimplemented)


# Requirements
1. Python v3.4 or higher
2. Pip installer
3. Chrome v120.x `(Other browsers wont work!)` - only if you want to extract links your your CivitAI Download History.


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
│   test.py
│
├───CivitAI_Info_Files
│       _InfoFilesHere.txt
├───CSVs
│       _csv files go here.txt
│
├───src
│      chromelauncher.py
│      CSVFromInfoFIles.py
│      ModelsFromLocalSD.py
│      scrape-from-download-history.py
└───
```

# Install Prerequisites
```bash
cd CivitAI-DownloadLink-Extractor
```

```bash
pip install -r requirements.txt
```
## Method 1: Copying info files to Projects root dir
1. Copy all *.info files to [**CivitAI_Info_Files**](./CivitAI_Info_Files) directory. You do not need to seperate the info files based on model type, CSVs will do that for you!

2. Run CSVFromInfoFile.py 

```bash
python CSVFromInfoFiles.py
```

## Method 2: Stable Diffusion Path
> NOTE: ALL PATHS IN [`CONFIG.INI`](./config.ini) MUST BE ABSOLUTE PATHS
1. Edit `config.ini`.
```ini
[SD-DIR]
dir = <SD Folder Location>

[Output] # This is optional, Default is root dir/CSVs
dir = <Custom Output Dir>
```

---
# CSV Structure
1. All your CSVs are with the following format:

Sr.no | Model Name | Model URL
--- | --- | ---
1 | Realistic Vision V4.0 | https://civitai.com/api/download/models/114367
2 | ... | ...
3 | ... | ...


## Author Notes [BONUS]
- I made this script to use with Runpod.
- If you are looking to **batch download** these extracted models to **Runpod**, goto my `Better Faster Runpod` repository.