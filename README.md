# CivitAI-DownloadLink-Extractor
 Extract _CivitAI Model Download Links_ via:
 - [x] Info Files
 - [x] Stable Diffusion Directory
 - [ ] CivitAI Download History 

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



# Currently Supported format:
* '*.info' files (found in your lora/model folder if downloaded through any CivitAI extension)

# Requirements
1. Python 3 or higher

# How to use
1. Make sure you have all files required. 
   ```bash
   D:.
   │   config.ini
   │   CSVFromInfoFIles.py
   │   LICENSE
   │   local-config.ini
   │   ModelsFromLocalSD.py
   │   README.md
   │
   ├───CivitAI_Info_Files
   │       _InfoFilesHere.txt
   │
   ├───CSVs
   │       _csv files go here.txt
   └───
   ```

## Method 1: Copying info files to Projects root dir
1. Copy all *.info files to [**CivitAI_Info_Files**](../blob/master/CivitAI_Info_Files) directory. You do not need to seperate the info files based on model type, CSVs will do that for you!

2. Run CSVFromInfoFile.py 

```bash
python CSVFromInfoFiles.py
```

## Method 2: Stable Diffusion Path
> NOTE: ALL PATHS IN [`CONFIG.INI`](../blob/master/config.ini) MUST BE ABSOLUTE PATHS
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