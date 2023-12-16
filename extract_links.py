from src.civitai_download_link_extractor import *

if __name__ == "__main__":
    choice = int(input(
        "Choose how you would like to extract links:\n\
        [1] Civit AI Info Files\n\
        [2] Stable Diffusion Directory\n\
        [3] Civit AI Download History\n"
        ))
    
    match choice:
        case 1:
            info_files.main()
        case 2:
            local_SD.main()
        case 3:
            civitai_download_history.main()
            
