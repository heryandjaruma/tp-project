from email import header
from turtle import position
from classes.OvEntity import OvEntity
from pydub import AudioSegment
from pydub.playback import play
import os
from go_to import *
from env import *
import numpy as np
import pandas as pd

def do_overlay(oe1:OvEntity, oe2:OvEntity):
    # pd.set_option('display.max_rows',None)        # IF wanna see all row

    history = pd.DataFrame()

    oe1_aes = oe1.audio_entities()
    oe2_aes = oe2.audio_entities()

    # tell possible combination
    print(f'There will be {oe1.get_count_entities()*oe2.get_count_entities()} possible combinations.\nStart processing...')

    # loop for each oe1_aes
    file_count_process = 1
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
            print(f"Processing #{file_count_process} entity...")
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
            df_ori_main = ori_df.loc[ae1_start:ae1_end,:]            # main part
            df_ori_left = ori_df.loc[ae1_end+1:,:]             # will not have a value if the last iteration

            df_ori_main = df_ori_main.reset_index()            # reset set index only for main part
            df_combined = pd.DataFrame()            # initiate new df
            df_combined = pd.concat([df_ori_init])            # append init to the new df


            df1 = df_ori_main
            df2 = particle_df

            df1['unique_id'] = np.arange(0, df1.shape[0]*2,2)
            df2['unique_id'] = np.arange(1, df2.shape[0]*2,2)
            
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


            # ADD HISTORY to dataframe
            # * ask : history tuh buat track semua file atau misah" aja per file?
            row_history = np.array([
                # file1, file2, class1, class2, file_output
                oe1.get_csv_filename(), oe2.get_csv_filename(), oe1_ae.get__class(), oe2_ae.get__class(), export_name
            ])
            history_df = pd.DataFrame(row_history.reshape(1,-1))
            history = pd.concat([history, history_df])            # append to df

            inc_particle = inc_particle + 1
            file_count_process = file_count_process + 1
        inc_ori = inc_ori + 1
    
    # EXPORT HISTORY
    oe1_filename = oe1.get_csv_filename()
    oe2_filename = oe2.get_csv_filename()
    export_history_name = oe1_filename[:-4] + '_OVERLAP_' + oe2_filename[:-4] + '.csv'
    got_to_history_dev()
    history.to_csv(export_history_name, header=False, index=False)
    go_to_project_dir()
    print("Done Processing...")
        


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
            # export_audio_entities(oes[-1])

    go_to_project_dir()                             # go to project
    
    # check_all_objects(oes)
    # overlay(oes[0], oes[1])


    # oe = oes[5]
    # print(oe.get_df())
    # aes = oe.audio_entities()
    # ae = aes[0]
    # print(ae.get_df(), ae.get_origin())
    do_overlay(oes[0], oes[5])