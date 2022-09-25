import os
from go_to import *
from env import *
from pydub import AudioSegment
from pydub.playback import play
import pandas as pd

class AudioEntity:
    def __init__(self, foa:str, _class:str, time_start:int, time_end:int, entity_num:int) -> None:
        self.origin = foa

        self.fold = self.origin[:5]
        self.room = self.origin[6:11]
        self.mix = self.origin[12:18]
        self.ov = self.origin[19:22]

        self._class = _class
        self.time_start = time_start
        self.time_end = time_end
        self.entity_num = entity_num
        # self.naming = "_".join([self.fold,self.room,self.mix,'%03d' % int(self.time_start), '%03d' % int(entity_num + 1)]) + '.wav'
        self.naming = "_".join([self.fold,self.room,self.mix,'class%02d' % int(entity_num + 1)]) + '.wav'
        self.set_pandas_metadata()
    
    def get_origin(self):
        return self.origin
    def get_time_start(self):
        return self.time_start
    def get_time_end(self):
        return self.time_end
    def get_duration(self):
        return self.time_end-self.time_start
    def get_entity(self):
        return self.entity
    def get_fold(self):
        return self.fold
    def get_room(self):
        return self.room
    def get_mix(self):
        return self.mix
    def get_ov(self):
        return self.ov
    def get_naming(self):
        return self.naming
    def get__class(self):
        return self._class
    
    def set_pandas_metadata(self):
        go_to_metadata_dir()
        # self.df = pd.read_csv(self.origin[:-3]+'csv', header=None,index_col=0)
        self.df = pd.read_csv(self.origin[:-3]+'csv', header=None)
        self.df.columns = ['Frm', 'Class', 'Track', 'Azmth', 'Elev']
        self.df = self.df.set_index('Frm')
        self.df = self.df.loc[self.time_start:self.time_end,:]
        self.df = self.df.reset_index()
        go_to_project_dir()
    def get_df(self):
        return self.df
    
    def create_me(self):
        go_to_foa_dir()
        audio = AudioSegment.from_file(self.origin)
        channels = audio.split_to_mono()
        channels = channels[0].split_to_mono()
        entity = channels[0]
        self.entity = entity[self.time_start*100 : self.time_end*100]

        self.channels = self.entity.channels
        self.frame_rate = self.entity.frame_rate
        self.sample_width = self.entity.sample_width
        self.set_channels = 2
        # print(f'time_start:{self.time_start} | time_end:{self.time_end}')
        go_to_project_dir()
    
    def export_self(self):
        self.create_me()
        go_to_audio_entities_dev()

        # EXPORT
        if self.naming in os.listdir():
            print(f'[{self.naming}] already exported...')
        else:
            print(f'[{self.naming}] exported...')

        self.entity.export(self.naming, format="wav")
        go_to_project_dir()

    def play(self):
        go_to_audio_entities_dev()
        play(self.entity)
        go_to_project_dir()