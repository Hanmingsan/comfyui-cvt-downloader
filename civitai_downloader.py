import os
import folder_paths
import requests
import re

class CivitaiDownloader:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        models_folders = [d for d in os.listdir(folder_paths.models_dir) if os.path.isdir(os.path.join(folder_paths.models_dir, d))]
        return {
            "required": {
                # Format: "name": ("TYPE", {"default": value, "min": min, "max": max})
                "model_url": ("STRING", {"multiline": False, "default": "model_url",}),
                "API_key" : ("STRING", {"multiline": False, "default": "",}),
                
                "save_dir": (models_folders,),
            },
            "optional": {
                "file_name":("STRING", {"multiline": False, "default": "",}), # this is depricated as there is a model name given by cvt. maybe one kindly as you would like to realize this function?
            },
            "hidden":   {
                
            }
        }
        
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("download_path",)
    FUNCTION = "download_model_CVT"
    CATEGORY = "Comfy_Model_Downloader"
    
    def download_model_CVT(self, model_url, api_key, save_dir, file_name="",):
        
        try:
            if re.match(r"^(https:\/\/civitai.com\/api\/download\/models\/\d+\?)?\w+\=\w+(\&\w+\=\w+)*$", model_url):
                # This case is for full params
                r = requests.get(model_url+f"&token={api_key}")
                if not r.status_code == 200:
                    raise ValueError(f"Download failed with http code {r.status_code}")
                    
                # Get file name here!
                if not file_name:
                    if "Content-Disposition" in r.headers:
                        if re.findall(r'filename="?([^"]+)"?', r.headers["Content-Disposition"]):
                            file_name = re.findall(r'filename="?([^"]+)"?', r.headers["Content-Disposition"])[0]
                        else:
                            raise ValueError("You did not name your file, nor did cvt...")
                    else:
                        raise ValueError("You did not name your file, nor did cvt...")
                        
                with open(os.path.join(folder_paths.models_dir, save_dir, file_name), 'xb') as f:
                    for chunk in r.iter_content(chunk_size=1024*1024):
                        f.write(chunk)
                    
            elif re.match(r"^(https:\/\/civitai.com\/api\/download\/models\/\d+)?$", model_url):
                # This case no extra params
                r = requests.get(model_url+f"?token={api_key}")
                if not r.status_code == 200:
                    raise ValueError(f"Download failed with http code {r.status_code}")
                    
                # Get file name here!
                if not file_name:
                    if "Content-Disposition" in r.headers:
                        if re.findall(r'filename="?([^"]+)"?', r.headers["Content-Disposition"]):
                            file_name = re.findall(r'filename="?([^"]+)"?', r.headers["Content-Disposition"])[0]
                        else:
                            raise ValueError("You did not name your file, nor did cvt...")
                    else:
                        raise ValueError("You did not name your file, nor did cvt...")
                with open(os.path.join(folder_paths.models_dir, save_dir, file_name), 'xb') as f:
                    for chunk in r.iter_content(chunk_size=1024*1024):
                        f.write(chunk)
            
            else:
                raise RuntimeError("What was going on?")
        
            return f"Model successfully downloaded into {os.path.join(folder_paths.models_dir, save_dir, file_name)}"
        
        except FileNotFoundError:
            return "file not found"
        
        except ValueError as e:
            return f"download failed due to {e}"
            
        except RuntimeError as e:
            return "idk..."
            
        except:
            return "idk...idk..."


NODE_CLASS_MAPPINGS = {
    "CivitaiDownloader": CivitaiDownloader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CivitaiDownloader": "Civitai Model Downloader"
}
