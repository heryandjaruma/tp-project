from turtle import position
from classes.OvEntity import OvEntity
from pydub import AudioSegment
from pydub.playback import play
import os
from go_to import *
from env import *
import numpy as np
import pandas as pd

# # TODO: combine 2 audio entities
# def overlay(oe1:OvEntity, oe2:OvEntity, testing=True):
#     # overlap_csv(entity1, entity2)


#     oe1_aes = oe1.audio_entities()
#     oe2_aes = oe2.audio_entities()
#     go_to_foa_dir()                                 # go to foa

#     #* testing=True means only one main audio will be processed
#     if testing == True:
#         audio_main = AudioSegment.from_file(oe1.get_foa())
#         audio_main = audio_main.split_to_mono()
#         audio_main = audio_main[0]
#         go_to_project_dir()                         # go to project
        
#         count = 1
#         for entity2_ae in oe2_aes:
#             go_to_audio_entities_dev()              # go to audio entity
#             audio_particle = AudioSegment.from_file(entity2_ae.get_naming())
#             overlayed = audio_main.overlay(audio_particle, position = oe1_aes[0].get_time_start()*100)

#             go_to_mix_dev()                         # go to mix_dev
#             overlayed.export("_".join([entity2_ae.get_fold(), entity2_ae.get_room(), entity2_ae.get_mix(), 'ov2','%03d' % count]) + '.wav')
#             count = count + 1
#     else:
#         count = 1
#         for entity1_index, entity1_ae in enumerate(entity1_aes):
#             audio_main = AudioSegment.from_file(entity1.get_foa())
#             audio_main = audio_main.split_to_mono()
#             audio_main = audio_main[0]
#             go_to_project_dir()                     # go to project
#             for entity2_ae in entity2_aes:
#                 go_to_audio_entities_dev()
#                 audio_particle = AudioSegment.from_file(entity2_ae.get_naming())

#                 #! TODO : do overlay algorithm here
#                 overlayed = audio_main.overlay(audio_particle, position=entity1_aes[entity1_index].get_time_start()*100)
#                 go_to_mix_dev()                     # go to mix_dev
#                 overlayed.export("_".join([entity2_ae.get_fold(), entity2_ae.get_room(), entity2_ae.get_mix(), 'ov2','%03d' % count]) + '.wav')
#                 count = count + 1
    
#     go_to_project_dir()                             # go to project
#     print("All process done...")

def do_overlay(oe1:OvEntity, oe2:OvEntity):
    oe1_aes = oe1.audio_entities()
    oe2_aes = oe2.audio_entities()

    # tell possible combination
    print(f'There will be {oe1.get_count_entities()*oe2.get_count_entities()} possible combinations')

    # loop for each oe1_aes
    inc_ori = 1
    for oe1_ae in oe1_aes:
        ori_df = oe1.get_df()   # get oe1's df
        go_to_foa_dir()
        ori_audio = AudioSegment.from_file(oe1.get_foa())   # get oe1's original audio
        go_to_project_dir()             # go to project
        ori_audio = ori_audio.split_to_mono()
        ori_audio = ori_audio[0]

        # get start, end, duration for oe1
        ae1_start = oe1_ae.get_time_start()
        ae1_end = oe1_ae.get_time_end()
        ae1_duration = ae1_end-ae1_start

        inc_particle = 1
        for iter_num, oe2_ae in enumerate(oe2_aes):
            # print('========================================================== Loop -', iter_num,'\n')

            particle_df = oe2_ae.get_df()   # get oe2's df
            go_to_audio_entities_dev()      # go to audio entities
            particle_audio = AudioSegment.from_file(oe2_ae.get_naming())   # get oe2's particle audio
            go_to_project_dir()

            

            # get start, end, duration for oe2
            ae2_start = oe2_ae.get_time_start()
            ae2_end = oe2_ae.get_time_end()
            ae2_duration = ae2_end-ae2_start


            ori_df = ori_df.set_index('Frm')            # use frm as index

            df_ori_init = ori_df.loc[:ae1_start-1,:]             # will have a value if not the first iteration
            # print('cut start :', ae1_start)
            df_ori_main = ori_df.loc[ae1_start:ae1_end,:]            # main part
            df_ori_left = ori_df.loc[ae1_end+1:,:]             # will not have a value if the last iteration
            # print('cut end :', ae1_end)
            # print("INIT")
            # print(df_ori_init)
            # print("ORI")
            # print(df_ori_main)
            # print("LEFT")
            # print(df_ori_left)


            df_ori_main = df_ori_main.reset_index()            # reset set index only for main part
            # particle_df = particle_df.set_index('Frm')


            df_combined = pd.DataFrame()            # initiate new df

            df_combined = pd.concat([df_ori_init])            # append init to the new df
            # print("COMBINED")
            # print(df_combined)

            # pd.set_option('display.max_rows',None)

            df1 = df_ori_main
            df2 = particle_df

            df1['unique_id'] = np.arange(0, df1.shape[0]*2,2)
            df2['unique_id'] = np.arange(1, df2.shape[0]*2,2)

            # ! START OVERLAY AUDIO
            

            if ae1_duration < ae2_duration:
                df2['Frm'] = df1['Frm']
                particle_audio = particle_audio[:ae1_duration*100]
            else:
                df2['Frm'] = df1['Frm'].iloc[:ae1_duration]


            new_df = pd.concat([df1,df2])
            new_df = new_df.sort_values(by=['unique_id'])
            # print(new_df)
            new_df = new_df.drop(columns='unique_id')
            new_df = new_df.dropna()
            new_df['Frm'] = new_df['Frm'].astype(int)
            new_df = new_df.set_index('Frm')
            # print(new_df)

            df_combined = pd.concat([df_combined, new_df])
            df_combined = pd.concat([df_combined, df_ori_left])

            ori_df = ori_df.reset_index()            # reset so index became int again

            # EXPORT CSV
            export_name = oe1.get_csv_filename().replace('ov1', 'ov2_%03d_%03d' % (inc_ori, inc_particle))
            go_to_metadata_dir()
            df_combined.to_csv(export_name,header=False)
            go_to_project_dir()


            # EXPORT AUDIO
            overlayed = ori_audio.overlay(particle_audio, position=ae1_start*100)
            go_to_mix_dev()
            overlayed.export("_".join([oe1_ae.get_fold(), oe1_ae.get_room(), oe1_ae.get_mix(), '%03d_%03d' % (inc_ori, inc_particle)]) + '.wav')
            go_to_project_dir()



            # print(df_combined)
            # print('==========================================================\n')
            # input()
            inc_particle = inc_particle + 1
        inc_ori = inc_ori + 1
            
        


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
        if 'ov2' not in item:
            oes.append(OvEntity(item))
            export_audio_entities(oes[-1])

    go_to_project_dir()                             # go to project
    
    # check_all_objects(oes)
    # overlay(oes[0], oes[1])


    # oe = oes[5]
    # print(oe.get_df())
    # aes = oe.audio_entities()
    # ae = aes[0]
    # print(ae.get_df(), ae.get_origin())
    # do_overlay(oes[0], oes[5])