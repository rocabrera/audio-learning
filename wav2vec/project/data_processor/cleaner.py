import os
import numpy as np
import pandas as pd
from pathlib import Path

from p_tqdm import p_map
from tqdm import tqdm
from pydub import AudioSegment
from sklearn.model_selection import train_test_split

tqdm.pandas()

class CreateTidyDataset:
    
    def __init__(self, databases):
        
        self.databases = databases
        
    def create_folder(self, path):
        Path(path).mkdir(parents=True, exist_ok=True)
        return path
    
    def is_folder_created(self, path, force:bool):
        if force: return False
        else: return Path(path).is_dir()
        
    def save_file_path_format(self,file, path):
        filename, _ = os.path.splitext(os.path.basename(file))
        new_file_path = os.path.join(path,filename+".wav")
        return new_file_path
    
    def mp3_convert(self, file, path):
        sound = AudioSegment.from_mp3(file)
        new_file_path = self.save_file_path_format(file, path)
        sound.export(new_file_path, format="wav")
    
    def flac_convert(self, file, path):
        sound = AudioSegment.from_file(file, format='flac')
        new_file_path = self.save_file_path_format(file, path)
        sound.export(new_file_path, format="wav")
        
    def converter_audio(self,n_cores=4):
        
        conver_mapper = {".mp3": self.mp3_convert, ".flac": self.flac_convert}
                
        for idx, (database, force) in enumerate(self.databases):
            print(f"Base {idx}:")
            path = os.path.join("data", "tidy", database.basename)
            if not self.is_folder_created(path, force):
                df = database.parse_data()
                path = self.create_folder(path)
                convert = conver_mapper[database.ext]
                
                # convert files
#                 files_split = np.array_split(df["file"], n_cores)
#                 _ = p_map(lambda x: convert(x, path), df["file"])
  
                df["file"].progress_apply(convert, args=[path])
                
    def __data_base_with_new_path(self, database):
        folder_path = os.path.join("data", "tidy", database.basename)
        df = database.parse_data()
        return df.assign(file=df["file"].apply(self.save_file_path_format, args=[folder_path]))

    def parse_datasets(self, test_size:float=0.1):
        
        df = pd.concat([self.__data_base_with_new_path(database) for database, _ in self.databases], ignore_index=True)
        return train_test_split(df, test_size=test_size)
            
