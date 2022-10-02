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

# CLASS ATTRIBUTES
# csv_filename
# foa
# fold
# room
# mix
# ov
# counter
# df
# entity
# channels
# frame_rate
# sample_width
# count_entities
# AudioEntities[]

class OvEntity:
    def __init__(self, csv_filename:str) -> None:
        self.csv_filename = csv_filename
        self.foa = self.csv_filename[:-4]+r'.wav'
        self.fold = self.csv_filename[:5]
        self.room = self.csv_filename[6:11]
        self.mix = self.csv_filename[12:18]
        self.ov = self.csv_filename[19:22]
        self.counter = 1
        self.set_pandas_metadata()                              # read metadata
        self.set_audio_entitites()                              # creating audio entities
        
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
    def get_entity(self):
        return self.entity
    def get_counter(self):
        return self.counter
    
    def increase_counter(self):
        self.counter = self.counter + 1

    def set_pandas_metadata(self):
        go_to_metadata_dir()
        self.df = pd.read_csv(self.csv_filename, header=None)
        self.df.columns = ['Frm', 'Class', 'Track', 'Azmth', 'Elev']
        go_to_project_dir()
    
    def create_me(self):
        go_to_foa_dir()
        audio = AudioSegment.from_file(self.foa)
        go_to_project_dir()
        channels = audio.split_to_mono()
        channels = channels[0].split_to_mono()
        self.entity = channels[0]
        self.channels = self.entity.channels
        self.frame_rate = self.entity.frame_rate
        self.sample_width = self.entity.sample_width
        self.set_channels = 2

    def set_audio_entitites(self):
        # TODO: process ov entity into audio entities
        self.count_entities = 0                                 # ! to count how many entities AE has
        self.AudioEntities = []                                 # ! list for AE

        existed_class = set()                                   # ! use set to prevent class duplicate

        first_row = self.df.iloc[0]                             # ! prepare first row' class as start point
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
                time_start = time_end = row['Frm']
                class_before = row['Class']

        new_entity = AudioEntity(self.foa,class_before,time_start,time_end,self.count_entities)
        # ! before append to the main list, check the availibility on the existed_class
        if new_entity.get__class() not in existed_class:
            self.AudioEntities.append(new_entity)
            existed_class.add(new_entity.get__class())
            self.count_entities = self.count_entities + 1
        time_start = time_end = row['Frm']
        class_before = row['Class']