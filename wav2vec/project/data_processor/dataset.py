import re
import os
import json
import pandas as pd
from glob import glob

from abc import ABC, abstractmethod

class DataBase(ABC):
    
    @abstractmethod
    def make_tidy(self):
        pass
    
    @abstractmethod
    def parse_data(self) -> pd.DataFrame:
        pass
    
class MLS(DataBase):
    
    ext = ".flac" 
    basename = "multi_speech_librespeech"
    
    def __init__(self, data_train_dir, data_test_dir, data_dev_dir):

        self.train_path = data_train_dir
        self.test_path = data_test_dir
        self.dev_path = data_dev_dir
        
    def _create_path(self, path_type:str, audio_code:str):
    
        match = re.search("(\d+)_(\d+)_(\d+)",audio_code)
        return os.path.join(path_type, "audio", match.group(1), match.group(2), "".join([audio_code, self.ext]))

    def _parse_type(self, path_type:str, type_:str) -> pd.DataFrame:
        path_label = os.path.join(path_type, "transcripts.txt")
        
        df = pd.read_csv(path_label, sep="\t",header=None,names=["audio_code", "text"])    
        df = df.assign(**{"type":type_,
                          "file":df.audio_code.apply(lambda x: 
                                                           self._create_path(path_type,x))
                         })
        return df.filter(["file", "text", "type"])
    
    def make_tidy(self):
        pass
    
    def parse_data(self) -> pd.DataFrame:
        
        df_train = self._parse_type(self.train_path, "train")
        df_test = self._parse_type(self.test_path, "test")
        df_dev = self._parse_type(self.dev_path, "dev")
    
        return pd.concat([df_train, df_test, df_dev], ignore_index=True).assign(base=self.basename)

class CommonVoice(DataBase):
    
    ext = ".mp3"    
    basename = "common_voice"
    
    def __init__(self, main_path):

        self.train_path = os.path.join(main_path, "train.tsv")
        self.test_path = os.path.join(main_path, "test.tsv")
        self.dev_path = os.path.join(main_path, "validated.tsv")
        self.audios_path = os.path.join(main_path, "clips")
        
    def _create_path(self, audio_name):
        return os.path.join(self.audios_path, audio_name)

    def _parse_type(self, df_path, type_): 
        
        df = pd.read_csv(df_path, sep = "\t")
        return (df.assign(**{"type":type_, "file":df["path"].apply(self._create_path)})
                  .rename(columns={"sentence":"text"})
                  .filter(["file", "text", "type"]))
    
    def make_tidy(self):
        pass
    
    def parse_data(self) -> pd.DataFrame: 
        
        df_train = self._parse_type(self.train_path, "train")
        df_test = self._parse_type(self.test_path,"test")
        df_dev = self._parse_type(self.dev_path,"dev")
        
        return pd.concat([df_train, df_test, df_dev], ignore_index=True).assign(base=self.basename)