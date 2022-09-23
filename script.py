from turtle import position
from classes.OvEntity import OvEntity
from pydub import AudioSegment
from pydub.playback import play
import os
from go_to import *
from env import *
import numpy as np
import pandas as pd

# project path

# # TODO: combine 2 csvs
# def overlap_csv(e1:OvEntity, e2:OvEntity):
#     e1_aes = e1.audio_entities()
#     e2_aes = e2.audio_entities()

#     df1 = e1.get_pd()
#     df1 = df1.set_index('Frm')
#     df2 = e2.get_pd()

#     df_combined = pd.DataFrame()

#     for e2_ae in e2_aes:
#         target_timestamp = [e2_ae.get_time_start(), e2_ae.get_time_end()]
        
#         for e1_ae in e1_aes:
#             start = e1_ae.get_time_start()
#             end = e1_ae.get_time_end()
#             if start!=target_timestamp[0] and end!=target_timestamp[1]:
#                 pd_particle = df1.loc[start:end,:]
#                 df_combined = pd.concat([df_combined, pd_particle])
#             else:
#                 print('asdf')
#                 if (end-start) > (target_timestamp[1]-target_timestamp[0]):
#                     for row in e2.get_pd().iterrows():
#                         print(row)

#     pd.set_option('display.max_rows',None)
#     print(df_combined)
    
    


#     # start = e1_aes[0].get_time_start()
#     # end1 = e1_aes[0].get_time_end()
#     # df1 = df1.loc[start:end1,:]
#     # print(df1)


#     go_to_metadata_dir()                            # go to metadata





# # TODO: combine 2 audio entities
# def overlay(entity1:OvEntity, entity2:OvEntity, testing=True):
#     # overlap_csv(entity1, entity2)


#     # entity1_aes = entity1.audio_entities()
#     # entity2_aes = entity2.audio_entities()
#     # go_to_foa_dir()                                 # go to foa

#     # #* testing=True means only one main audio will be processed
#     # if testing == True:
#     #     audio_main = AudioSegment.from_file(entity1.get_foa())
#     #     audio_main = audio_main.split_to_mono()
#     #     audio_main = audio_main[0]
#     #     go_to_project_dir()                         # go to project
        
#     #     count = 1
#     #     for entity2_ae in entity2_aes:
#     #         go_to_audio_entities_dev()              # go to audio entity
#     #         audio_particle = AudioSegment.from_file(entity2_ae.get_naming())
#     #         overlayed = audio_main.overlay(audio_particle, position = entity1_aes[0].get_time_start()*100)

#     #         go_to_mix_dev()                         # go to mix_dev
#     #         overlayed.export("_".join([entity2_ae.get_fold(), entity2_ae.get_room(), entity2_ae.get_mix(), 'ov2','%03d' % count]) + '.wav')
#     #         count = count + 1
#     # else:
#     #     count = 1
#     #     for entity1_index, entity1_ae in enumerate(entity1_aes):
#     #         audio_main = AudioSegment.from_file(entity1.get_foa())
#     #         audio_main = audio_main.split_to_mono()
#     #         audio_main = audio_main[0]
#     #         go_to_project_dir()                     # go to project
#     #         for entity2_ae in entity2_aes:
#     #             go_to_audio_entities_dev()
#     #             audio_particle = AudioSegment.from_file(entity2_ae.get_naming())

#     #             #! TODO : do overlay algorithm here
#     #             overlayed = audio_main.overlay(audio_particle, position=entity1_aes[entity1_index].get_time_start()*100)
#     #             go_to_mix_dev()                     # go to mix_dev
#     #             overlayed.export("_".join([entity2_ae.get_fold(), entity2_ae.get_room(), entity2_ae.get_mix(), 'ov2','%03d' % count]) + '.wav')
#     #             count = count + 1
    
#     # go_to_project_dir()                             # go to project
#     # print("All process done...")
    

# TODO: export all Audio Entities in a specified Ov Entity
def export_audio_entities(oe:OvEntity):
    print(f'Total of {oe.get_count_entities()} audio entities will be exported\nProceed?[y/n]')
    confirm = input().lower()
    if confirm == 'y':
        for ae in oe.audio_entities():
            ae.export_self()
    else:
        print('Export cancelled...')
        pass


# TODO: check Ov Entity array
def check_all_objects(oe_array):
    for ov in oe_array:
        print(f'  {ov.get_csv_filename()}')
        print('==================================')
        for ae in ov.audio_entities():
            print(f'    {ae.get_naming()}')
        print(f' [classes: {ov.get_count_entities()}]\n')


# TODO: main
if __name__ == '__main__':
    oes = []
    go_to_metadata_dir()                            # go to metadata

    # TODO: creating object for each file in \metadata_dev
    for item in os.listdir():
        oes.append(OvEntity(item))
        # export_audio_entities(oes[-1])

    go_to_project_dir()                             # go to project
    
    # check_all_objects(oes)
    # overlay(oes[0], oes[1])
    oe = oes[1]
    aes = oe.audio_entities()
    ae = aes[0]
    print(ae.get_pd())