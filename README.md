# CivitAI-DownloadLink-Extractor
 Extract CivitAI Model Links via various sources.

# Currently Supported format:
* '*.info' files (found in your lora/model folder if downloaded through any CivitAI extension)

# Requirements
1. Python 3 or higher

# How to use
1. Make sure you have all files required. 
   ```bash
    D:/CivitAi-DownloadLink-Extractor
    │   .gitattributes
    │   .gitignore
    │   CSVFromInfoFIles.py
    │   LICENSE
    │   README.md
    │   
    ├───CivitAI_Info_Files
    │       _InfoFilesHere.txt
    │       
    └───CSVs
            ckpts.csv
            cnetmodels.csv
            LORAs.csv
            TextualInversions.csv
            _csv files go here.txt
   ```

2. Copy all *.info files to **CivitAI_Info_Files** directory. You do not need to seperate the info files based on model type, CSVs will do that for you!

3. Run CSVromInfoFile.py 
```
python CSVFromInfoFiles.py
```
4. All your CSVs are ready with the following format:

Sr.no | Model Name | Model URL
--- | --- | ---
1 | Realistic Vision V4.0 | https://civitai.com/api/download/models/114367
2 | ... | ...
3 | ... | ...

## Future Work
* Work directly with links
* Work with model name only using CivitAI Search

## Author Notes
I made this script to use with Runpod.
If you are looking for the same, goto my `Runpod Setup Files` repository. 