import os
import numpy as np
import pandas as pd
from colorama import Fore
from pydub import AudioSegment
from pydub.playback import play

from env import *
from go_to import *
from filename_rule import *
from classes.OvEntity import OvEntity



# TODO: will get all files in the given range implicitly
def get_all_files_in_metadata_dev(first_fold_number:int, last_fold_number:int):
    go_to_metadata_dir()
    all_list = [file for file in os.listdir() if 'ov2' not in file]
    returned_list_list = []
    
    for item in range(first_fold_number, last_fold_number+1):
        returned_list = [file for file in all_list if ('fold' + str(item)) in file]
        if returned_list:
            returned_list_list.append(returned_list)
        else:
            print(Fore.RED, 'fold', item, 'does not exist... try checking your file', Fore.WHITE)
        
    go_to_project_dir()                             # go to project
    return returned_list_list

def init_all_objects(list_of_files: list[list], export_audio_entities = True):
    # go_to_metadata_dir()                            # go to metadata
    main_object_list = []
    for outer_item in list_of_files:
        object_list = []
        for inner_item in outer_item:
            object_list.append(OvEntity(inner_item))
            if export_audio_entities:
                export_audio_entities(object_list[-1])
        main_object_list.append(object_list)
    return main_object_list

# * PERMUTATION INDEXING is used to do permutation of folder name (1-5)
def get_permutation_indexing(first_fold_number:int, last_fold_number:int):
    listed = list(range(first_fold_number,last_fold_number+1))
    combination = np.array(np.meshgrid(listed, listed)).T.reshape(-1,2)
    combination = np.sort(combination)
    combination = np.unique(combination, axis = 0)
    combination = [item for item in combination if item[0] != item[1]]
    return combination

def get_combination_folder_indexing(list_of_object1:list, list_of_object2:list):
    return np.array(np.meshgrid(list_of_object1, list_of_object2)).T.reshape(-1,2)


def overlay_all_objects(list_of_list_object: list, first_fold_number:int, last_fold_number:int):

    permutation_indexing = get_permutation_indexing(first_fold_number, last_fold_number)
    
    print('This process will combine folder in this manner:')
    for item in permutation_indexing:
        print(item)

    while True:
        confirm_folder = input('Execute now?[y/n]')
        if confirm_folder=='y':
            break
        elif confirm_folder=='n':
            return
        else:
            continue

    for object_indexing in permutation_indexing:

        # combination = np.array(np.meshgrid(object_indexing[0], object_indexing[1])).T.reshape(-1,2)
        # combination = np.array(np.meshgrid(list_of_list_object[object_indexing[0]-1], list_of_list_object[object_indexing[1]-1])).T.reshape(-1,2)
        combination_indexing = get_combination_folder_indexing(list_of_list_object[object_indexing[0]-1], list_of_list_object[object_indexing[1]-1])

        print('This process will combine mixes in this manner:')
        for item in combination_indexing:
            print(item)

        while True:
            confirm_mix = input('Execute now?[y/n]')
            if confirm_mix=='y':
                break
            elif confirm_mix=='n':
                return
            else:
                continue


        for i, item in enumerate(combination_indexing):
            # print(i, item[0].get_csv_filename(), item[1].get_csv_filename())
            do_overlay(item[0], item[1])
            print('')
        # do_overlay(list_of_list_object[object_indexing[0]-1], list_of_list_object[object_indexing[1]-1])



def do_overlay(oe1:OvEntity, oe2:OvEntity):

    history = pd.DataFrame()

    oe1_aes = oe1.audio_entities()
    oe2_aes = oe2.audio_entities()

    # tell possible combination
    print('Now processing', Fore.LIGHTMAGENTA_EX, oe1.get_csv_filename(), Fore.WHITE , 'with', Fore.LIGHTMAGENTA_EX, oe2.get_csv_filename(), Fore.WHITE)
    print(f'There will be {oe1.get_count_entities()*oe2.get_count_entities()} possible combinations.\nStart processing...')

    # loop for each oe1_aes
    file_count_process = 1

    increment_original = 1          # increment for original_audio loop

    for oe1_ae in oe1_aes:


        # OE1
        # ##########################################################################
        ori_df = oe1.get_df()   # get oe1's df
        go_to_foa_dir()
        original_audio = AudioSegment.from_file(oe1.get_foa())   # get oe1's original audio
        go_to_project_dir()             # go to project
        original_audio = original_audio.split_to_mono()
        original_audio = original_audio[0]

        # get start, end, duration for ae1
        ae1_start = oe1_ae.get_time_start()
        ae1_end = oe1_ae.get_time_end()
        ae1_duration = ae1_end-ae1_start
        # ##########################################################################


        increment_particle = 1      # increment for particle_audio loop


        for iter_num, oe2_ae in enumerate(oe2_aes):

            # Notify the running process
            # ##########################################################################
            print(Fore.GREEN, f"Processing #{file_count_process} entity...", Fore.WHITE)
            print('\tCombining class', Fore.LIGHTYELLOW_EX, oe1_ae.get__class(), 'of', oe1.get_foa(), Fore.WHITE, 'with class', Fore.LIGHTYELLOW_EX, oe2_ae.get__class(), 'of', oe2.get_foa(), Fore.WHITE)
            # ##########################################################################



            # OE2
            # ##########################################################################
            particle_df = oe2_ae.get_df()   # get oe2's df
            go_to_audio_entities_dev()      # go to audio entities
            particle_audio = AudioSegment.from_file(oe2_ae.get_naming())   # get oe2's particle audio
            go_to_project_dir()
            particle_audio = particle_audio.split_to_mono()
            particle_audio = particle_audio[0]

            # get start, end, duration for ae2
            ae2_start = oe2_ae.get_time_start()
            ae2_end = oe2_ae.get_time_end()
            ae2_duration = ae2_end-ae2_start
            # ##########################################################################




            # process original audio into -> initial | main | left
            # ##########################################################################
            ori_df = ori_df.set_index('Frm')            # use frm as index
            df_ori_init = ori_df.loc[:ae1_start-1,:]             # will have a value if not the first iteration
            df_ori_main = ori_df.loc[ae1_start:ae1_end,:]            # main part
            df_ori_left = ori_df.loc[ae1_end+1:,:]             # will not have a value if the last iteration

            df_ori_main = df_ori_main.reset_index()            # reset set index only for main part
            df_combined = pd.DataFrame()            # initiate new df
            df_combined = pd.concat([df_ori_init])            # append init to the new df
            # ##########################################################################




            # algorithm to overlap audio in csv
            # ##########################################################################
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
            new_df = new_df.drop(columns='unique_id')
            new_df = new_df.dropna()
            new_df['Frm'] = new_df['Frm'].astype(int)
            new_df = new_df.set_index('Frm')

            df_combined = pd.concat([df_combined, new_df])
            df_combined = pd.concat([df_combined, df_ori_left])

            ori_df = ori_df.reset_index()            # reset index as int, not 'Frm' column
            # ##########################################################################



            # EXPORT CSV
            # ##########################################################################
            # csv_name_export = oe1.get_csv_filename().replace('ov1', 'ov2_%03d_%03d' % (increment_original, increment_particle))
            csv_name_export = export_overlapped_csv(oe1, oe2, increment_original, increment_particle)
            go_to_metadata_dir()
            df_combined.to_csv(csv_name_export, header=False)
            go_to_project_dir()
            print('\tOverlapped csv exported as', Fore.LIGHTMAGENTA_EX, csv_name_export, Fore.WHITE)
            # ##########################################################################



            # EXPORT AUDIO
            # ##########################################################################
            overlayed = original_audio.overlay(particle_audio, position=ae1_start*100)
            go_to_mix_dev()
            # audio_name_export = "_".join([oe1_ae.get_fold(), oe1_ae.get_room(), oe1_ae.get_mix(), 'ov2', '%03d_%03d' % (increment_original, increment_particle)]) + '.wav'
            audio_name_export = export_overlapped_audio(oe1_ae, oe2_ae, increment_original, increment_particle)
            overlayed.export(audio_name_export)
            print('\tOverlapped audio exported as', Fore.LIGHTBLUE_EX, audio_name_export, Fore.WHITE)
            go_to_project_dir()
            # ##########################################################################




            # ADD HISTORY to dataframe
            # ##########################################################################
            row_history = np.array([
                oe1.get_csv_filename(), oe2.get_csv_filename(), oe1_ae.get__class(), oe2_ae.get__class(), csv_name_export
            ])
            history_df = pd.DataFrame(row_history.reshape(1,-1))
            history = pd.concat([history, history_df])            # append to df
            # ##########################################################################



            # increment for each vars
            # ##########################################################################
            increment_particle = increment_particle + 1
            file_count_process = file_count_process + 1
            # ##########################################################################
        increment_original = increment_original + 1
        # ##########################################################################
    


    # EXPORT HISTORY
    # ##########################################################################
    oe1_filename = oe1.get_csv_filename()
    oe2_filename = oe2.get_csv_filename()
    # history_name_export = oe1_filename[:-4] + '_OVERLAP_' + oe2_filename[:-4] + '.csv'
    history_name_export = export_history(oe1_filename, oe2_filename)
    got_to_history_dev()
    history.to_csv(history_name_export, header=False, index=False)
    go_to_project_dir()
    # ##########################################################################



    # Notify process is done
    # ##########################################################################
    print('History exported', Fore.LIGHTMAGENTA_EX, history_name_export, Fore.WHITE)        
    # ##########################################################################


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
    print('')


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
    folder_start = 1
    folder_end = 2

    all_files = get_all_files_in_metadata_dev(folder_start, folder_end)

    # for i in all_files:
    #     print(i)

    all_objects = init_all_objects(all_files, export_audio_entities = False)

    # for i in all_objects:
    #     print(i)
    overlay_all_objects(all_objects, folder_start, folder_end)

    print('\nProgram exiting...')