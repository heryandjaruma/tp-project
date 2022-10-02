import os
import pandas as pd
from pydub import AudioSegment
from pydub.playback import play

from go_to import *
from filename_rule import export_particle_audio, export_particle_label_only

# CLASS ATTRIBUTES
# origin
# room
# mix
# ov
# class
# time_start
# time_end
# entity_num
# naming
# df
# entity
# channels
# frame_rate
# sample_width
# set_channel

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
        self.naming = export_particle_audio(self.fold, self.room, self.mix, self.ov, self._class)
        self.set_pandas_metadata()

        self.counter = 1
    
    def get_origin(self):
        return self.origin
    def get_time_start(self):
        return self.time_start
    def get_time_end(self):
        return self.time_end
    def get_duration(self):
        return self.time_end-self.time_start
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
    def get_df(self):
        return self.df
    def get_entity(self):
        return self.entity
    def get_export_cut(self):
        return self.particle_audio_cut
    
    def set_pandas_metadata(self):
        go_to_metadata_dir()
        df = pd.read_csv(self.origin[:-3]+'csv', header=None)
        go_to_project_dir()
        df.columns = ['Frm', 'Class', 'Track', 'Azmth', 'Elev']
        df = df.set_index('Frm')
        df = df.loc[self.time_start:self.time_end,:]
        self.df = df.reset_index()

    def create_me(self):
        go_to_foa_dir()
        audio = AudioSegment.from_file(self.origin)
        go_to_project_dir()
        channels = audio.split_to_mono()
        channels = channels[0].split_to_mono()
        entity = channels[0]
        self.entity = entity[self.time_start*100 : self.time_end*100]
        self.channels = self.entity.channels
        self.frame_rate = self.entity.frame_rate
        self.sample_width = self.entity.sample_width
        self.set_channels = 2    

    def export_self(self):
        self.create_me()
        go_to_audio_entities_dev()
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

    def export_cut_self(self, duration:int):
        self.particle_audio_cut = self.entity[:duration*100]
        particle_cut_name = export_particle_label_only(self.get_fold(), self.get_room(), self.get_mix(), self.get__class(), self.counter)
        self.counter = self.counter + 1
        go_to_wav_tunggal_cut()    
        self.particle_audio_cut.export(particle_cut_name)    # ! export the particle into wav_tunggal_cut
        go_to_project_dir()
        return particle_cut_name