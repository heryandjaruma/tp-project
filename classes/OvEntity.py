import os
import pandas as pd
from classes.AudioEntity import AudioEntity
from go_to import *
from pydub import AudioSegment
from pydub.playback import play

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

        self.fold = self.csv_filename[:5]
        self.room = self.csv_filename[6:11]
        self.mix = self.csv_filename[12:18]
        self.ov = self.csv_filename[19:22]

        self.set_pandas_metadata()        # read metadata
        self.set_audio_entitites()        # creating audio entities
        self.used = 0

        go_to_foa_dir()
        original_audio = AudioSegment.from_file(self.foa)   # get oe1's original audio
        go_to_project_dir()             # go to project
        original_audio = original_audio.split_to_mono()
        self.original_audio = original_audio[0]
    
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
        self.df = pd.read_csv(self.csv_filename, header=None)
        self.df.columns = ['Frm', 'Class', 'Track', 'Azmth', 'Elev']
        go_to_project_dir()
    def get_df(self):
        return self.df
    
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
    
    def get_export(self):
        return self.original_audio

    def set_audio_entitites(self):
        # TODO: process ov entity into audio entities
        self.count_entities = 0     # ! to count how many entities AE has
        self.AudioEntities = []     # ! list for AE

        # check if there's duplicate class
        existed_class = set()

        first_row = self.df.iloc[0]
        time_start = time_end = first_row['Frm']
        class_before = first_row['Class']

        for index, row in self.df.iterrows():
            if row['Class'] == class_before:
                # ! if the row has the same class before, which mean the audio is still running, then continue to the next row
                time_end = row['Frm']
                continue
            else:
                # ! create the entity first
                new_entity = AudioEntity(self.foa,class_before,time_start,time_end,self.count_entities)

                # ! before append to the main list, check the availibility of the newly created entity on the existed_class
                if new_entity.get__class() not in existed_class:
                    self.AudioEntities.append(new_entity)
                    existed_class.add(new_entity.get__class())
                    self.count_entities = self.count_entities + 1
                    # print(f'{dict[class_before]}--time_start:{time_start} until time_end:{time_end} with duration:{(time_end-time_start)/10}s')
                time_start = time_end = row['Frm']
                class_before = row['Class']

        new_entity = AudioEntity(self.foa,class_before,time_start,time_end,self.count_entities)
        # ! before append to the main list, check the availibility on the existed_class
        if new_entity.get__class() not in existed_class:
            self.AudioEntities.append(new_entity)
            existed_class.add(new_entity.get__class())
            self.count_entities = self.count_entities + 1

            # print(f'{dict[class_before]}--time_start:{time_start} until time_end:{time_end} with duration:{(time_end-time_start)/10}s')
        time_start = time_end = row['Frm']
        class_before = row['Class']
    
    def get_used(self):
        return self.used
    def use(self):
        self.used = self.used + 1