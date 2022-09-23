import os
import pandas as pd
from classes.AudioEntity import AudioEntity
from env import *
from go_to import *

dict = [
"alarm",
"crying baby",
"crash",
"barking dog",
"running engine",
"female scream",
"female speech",
"burning fire",
"footsteps",
"knocking on door",
"male scream",
"male speech",
"ringing phone",
"piano"
]


class OvEntity:
    def __init__(self, csv_filename:str) -> None:
        self.csv_filename = csv_filename
        
        self.foa = self.csv_filename[:-4]+r'.wav'

        # read metadata
        self.set_pandas_metadata()

        # creating audio entities
        self.set_audio_entitites()
    
    def go_to_metadata_dir(self):
        os.chdir(path_to_project_fold+r'\metadata_dev')
    def go_to_foa_dir(self):
        os.chdir(path_to_project_fold+r'\foa_dev')
    def go_to_audio_entities_dev(self):
        os.chdir(path_to_project_fold+r'\audio_entity_dev')
    def go_to_project_dir(self):
        os.path.dirname(path_to_project_fold)

    def set_pandas_metadata(self):
        go_to_metadata_dir()
        self.pd = pd.read_csv(self.csv_filename, header=None)
        self.pd.columns = ['Frm', 'Class', 'Track', 'Azmth', 'Elev']
        go_to_project_dir()
    def get_pd(self):
        return self.pd
    
    def get_csv_filename(self):
        return self.csv_filename
    def get_foa(self):
        return self.foa
        
    def get_fold(self):
        return self.fold
    def get_room(self):
        return self.room
    def get_mix(self):
        return self.mix
    def get_ov(self):
        return self.ov


    def get_count_entities(self):
        return self.count_entities
    def audio_entities(self):
        return self.AudioEntities
    def set_audio_entitites(self):
        # TODO: process ov entity into audio entities
        # self.AudioEntities = AudioEntity(self.project_path, self.csv_filename)
        self.count_entities = 0
        self.AudioEntities = []

        first_row = self.pd.iloc[0]
        time_start = time_end = first_row['Frm']
        class_before = first_row['Class']

        for index, row in self.pd.iterrows():
            if class_before == row['Class']:
                time_end = row['Frm']
                continue
            else:
                self.AudioEntities.append(AudioEntity(self.foa,class_before,time_start,time_end,self.count_entities))
                # print(f'{dict[class_before]}--time_start:{time_start} until time_end:{time_end} with duration:{(time_end-time_start)/10}s')
                time_start = time_end = row['Frm']
                class_before = row['Class']
                self.count_entities = self.count_entities + 1

        # final class append
        self.AudioEntities.append(AudioEntity(self.foa,class_before,time_start,time_end,self.count_entities))
        # print(f'{dict[class_before]}--time_start:{time_start} until time_end:{time_end} with duration:{(time_end-time_start)/10}s')
        time_start = time_end = row['Frm']
        class_before = row['Class']
        self.count_entities = self.count_entities + 1