import os
import numpy as np
import pandas as pd
from colorama import Fore
from pydub import AudioSegment
from pydub.playback import play

from go_to import *
from filename_rule import export_history, export_overlapped_audio, export_overlapped_csv, export_particle_label_only, export_particle_label_overlap
from classes.OvEntity import OvEntity



def get_counter(foldname):
    if foldname == 'fold1':
        return universal_counter_fold1
    if foldname == 'fold2':
        return universal_counter_fold2
    if foldname == 'fold3':
        return universal_counter_fold3
    if foldname == 'fold4':
        return universal_counter_fold4
    if foldname == 'fold5':
        return universal_counter_fold5
    if foldname == 'fold6':
        return universal_counter_fold6

def increase_counter(foldname):
    if foldname == 'fold1':
        universal_counter_fold1 = universal_counter_fold1 + 1
    if foldname == 'fold2':
        universal_counter_fold2 = universal_counter_fold2 + 1
    if foldname == 'fold3':
        universal_counter_fold3 = universal_counter_fold3 + 1
    if foldname == 'fold4':
        universal_counter_fold4 = universal_counter_fold4 + 1
    if foldname == 'fold5':
        universal_counter_fold5 = universal_counter_fold5 + 1
    if foldname == 'fold6':
        universal_counter_fold6 = universal_counter_fold6 + 1
        


def get_mix_counter(foldname):
    if foldname == 'fold1':
        return universal_counter_mix_fold1
    if foldname == 'fold2':
        return universal_counter_mix_fold2
    if foldname == 'fold3':
        return universal_counter_mix_fold3
    if foldname == 'fold4':
        return universal_counter_mix_fold4
    if foldname == 'fold5':
        return universal_counter_mix_fold5
    if foldname == 'fold6':
        return universal_counter_mix_fold6

def increase_mix_counter(foldname):
    if foldname == 'fold1':
        universal_counter_mix_fold1 = universal_counter_mix_fold1 + 1
    if foldname == 'fold2':
        universal_counter_mix_fold2 = universal_counter_mix_fold2 + 1
    if foldname == 'fold3':
        universal_counter_mix_fold3 = universal_counter_mix_fold3 + 1
    if foldname == 'fold4':
        universal_counter_mix_fold4 = universal_counter_mix_fold4 + 1
    if foldname == 'fold5':
        universal_counter_mix_fold5 = universal_counter_mix_fold5 + 1
    if foldname == 'fold6':
        universal_counter_mix_fold6 = universal_counter_mix_fold6 + 1

# TODO: clear screen
def clear_screen():
    os.system('cls||clear')

# TODO: export all Audio Entities in a specified Ov Entity
def export_audio_entities(oe:OvEntity, skip_confirm=False):
    if not skip_confirm:
        print(f'Total of {oe.get_count_entities()} audio entities will be exported\nProceed?[y/n]')
        confirm = input().lower()
        if confirm == 'y':
            for ae in oe.audio_entities():
                ae.export_self()
        else:
            print('Export cancelled...')
            pass
        print('')
    else:
        for ae in oe.audio_entities():
            ae.export_self()

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
            last_fold_number = last_fold_number-1
        
    go_to_project_dir()                             # go to project
    return returned_list_list, last_fold_number     #! RETURN list of list and last folder number that is valid

# TODO: to initialize all objects from files
def init_all_objects(list_of_files: list[list], export_audio = True, skip_confirm=False):
    main_object_list = []
    for outer_item in list_of_files:
        object_list = []
        for inner_item in outer_item:
            object_list.append(OvEntity(inner_item))

            if export_audio:        # ! if export_audio is true
                export_audio_entities(object_list[-1], skip_confirm)

        main_object_list.append(object_list)
    return main_object_list

# TODO: PERMUTATION INDEXING is used to do permutation between folders
def get_permutation_indexing(first_fold_number:int, last_fold_number:int):
    listed = list(range(first_fold_number,last_fold_number+1))
    combination = np.array(np.meshgrid(listed, listed)).T.reshape(-1,2)
    combination = np.sort(combination)
    combination = np.unique(combination, axis = 0)
    combination = [item for item in combination if item[0] != item[1]]
    return combination

# TODO: COMBINATION FOLDER INDEXING is used to do combination between objects
def get_combination_folder_indexing(list_of_object1:list, list_of_object2:list):
    return np.array(np.meshgrid(list_of_object1, list_of_object2)).T.reshape(-1,2)

# TODO: overlapping all objects according to folder permutation and object combination
def overlay_all_objects(list_of_list_object: list, first_fold_number:int, last_fold_number:int, skip_confirm=True):
    permutation_indexing = get_permutation_indexing(first_fold_number, last_fold_number)
    
    # if not skip_confirm:
    print('\nThis process will combine folder in this manner:')
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
        combination_indexing = get_combination_folder_indexing(list_of_list_object[object_indexing[0]-1], list_of_list_object[object_indexing[1]-1]) 

        if not skip_confirm:
            print('This process will combine mixes in this manner:')
            for item_arr in combination_indexing:
                print(f'\t{item_arr[0].get_foa()} -- {item_arr[1].get_foa()}')

            while True:
                confirm_mix = input('Execute now?[y/n]')
                if confirm_mix=='y':
                    break
                elif confirm_mix=='n':
                    return
                else:
                    continue

        for item in combination_indexing:
            do_overlay(item[0], item[1])            
            print('')

def get_increment_number_label_only(folder_number:int):
    go_to_wav_tunggal_cut()
    countfiles = 0
    for item in os.listdir():
        if folder_number in item:
            countfiles = countfiles+1
    return countfiles

def get_increment_number_label_overlap(folder_number:int):
    go_to_mix_wav_tunggal_cut_overlap()
    countfiles = 0
    for item in os.listdir():
        if folder_number in item:
            countfiles = countfiles+1
    return countfiles

# TODO: do the overlap main algorithm
def do_overlay(oe1:OvEntity, oe2:OvEntity):
    history = pd.DataFrame()

    oe1_aes = oe1.audio_entities()
    oe2_aes = oe2.audio_entities()

    # tell possible combination
    print('Now processing', Fore.LIGHTMAGENTA_EX, oe1.get_csv_filename(), Fore.WHITE , 'with', Fore.LIGHTMAGENTA_EX, oe2.get_csv_filename(), Fore.WHITE)
    print(f'There will be {oe1.get_count_entities()*oe2.get_count_entities()} possible combinations.\nStart processing...')

    increment = 1
    for oe1_ae in oe1_aes:
        # OE1
        ori_df = oe1.get_df()   # get oe1's df
        original_audio = oe1.get_export()

        # get start, end, duration for ae1
        ae1_start = oe1_ae.get_time_start()
        ae1_end = oe1_ae.get_time_end()
        ae1_duration = ae1_end-ae1_start

        for oe2_ae in oe2_aes:
            # Notify the running process
            print(Fore.GREEN, f"Processing #{increment} entity...", Fore.WHITE)
            print('\tCombining class', Fore.LIGHTYELLOW_EX, oe1_ae.get__class(), 'of', oe1.get_foa(), Fore.WHITE, 'with class', Fore.LIGHTYELLOW_EX, oe2_ae.get__class(), 'of', oe2.get_foa(), Fore.WHITE)

            # OE2
            particle_df = oe2_ae.get_df()   # get oe2's df
            particle_audio_df2 = oe2_ae.get_export()

            # get start, end, duration for ae2
            ae2_start = oe2_ae.get_time_start()
            ae2_end = oe2_ae.get_time_end()
            ae2_duration = ae2_end-ae2_start

            # process original audio into -> initial | main | left
            ori_df = ori_df.set_index('Frm')            # use frm as index
            df_ori_init = ori_df.loc[:ae1_start-1,:]             # will have a value if not the first iteration
            df_ori_main = ori_df.loc[ae1_start:ae1_end,:]            # main part
            df_ori_left = ori_df.loc[ae1_end+1:,:]             # will not have a value if the last iteration

            df_ori_main = df_ori_main.reset_index()            # reset set index only for main part
            df_combined = pd.DataFrame()            # initiate new df
            df_combined = pd.concat([df_ori_init])            # append init to the new df

            # algorithm to overlap audio in csv
            pd.set_option('display.max_rows', None)
            df1 = df_ori_main
            df2 = particle_df
            df1['unique_id'] = np.arange(0, df1.shape[0]*2,2)
            df2['unique_id'] = np.arange(1, df2.shape[0]*2,2)

            # determine which entity is longer
            if ae1_duration < ae2_duration:
                # ! entity df2 is longer, so df2 duration will be cut according to ae1 duration
                df2['Frm'] = df1['Frm']

                #TODO: export cut version of df2
                particle2_name = oe2_ae.export_cut_self(ae1_duration, get_counter(oe2_ae.get_fold()))
                increase_counter(oe2_ae.get_fold())
                #TODO: export original df1
                particle1_name = oe1_ae.export_cut_self(ae1_duration, get_counter(oe1_ae.get_fold()))
                increase_counter(oe1_ae.get_fold())

            else:
                # ! entity df1 is longer, so df1 frame will be copied into df2 frame, but the duration will be cut to match df2
                df2['Frm'] = df1['Frm'].iloc[:ae1_duration]

                #TODO: export cut version of df1
                particle1_name = oe1_ae.export_cut_self(ae2_duration, get_counter(oe1_ae.get_fold()))
                increase_counter(oe1_ae.get_fold())
                #TODO: export original of df2
                particle2_name = oe2_ae.export_cut_self(ae2_duration, get_counter(oe2_ae.get_fold()))
                increase_counter(oe2_ae.get_fold())

            # ! process to merge the df
            new_df = pd.concat([df1,df2])
            new_df = new_df.sort_values(by=['unique_id'])
            new_df = new_df.drop(columns='unique_id')
            # ! in case of df2 is longer, then the dropna will take effect
            # ! in case of df1 is longer, then dropna will take NO effect
            new_df = new_df.dropna()
            new_df['Frm'] = new_df['Frm'].astype(int)
            new_df = new_df.set_index('Frm')

            df_combined = pd.concat([df_combined, new_df])
            df_combined = pd.concat([df_combined, df_ori_left])

            ori_df = ori_df.reset_index()            # ! reset index as int, not 'Frm' column

            # EXPORT WAV_TUNGGAL_CUT_MERGE
            overlap = oe1_ae.get_export_cut()
            overlap = overlap.overlay(oe2_ae.get_export_cut())

            

            mix_increment = get_mix_counter(oe1.get_fold())

            # ! then overlap the audio which both now has the same length
            particle_overlap_name_export = export_particle_label_overlap(oe1_ae.get_fold(), oe1_ae.get_room(), oe1_ae.get_mix(), oe1_ae.get__class(), oe2_ae.get__class(), mix_increment)
            increase_mix_counter(oe1.get_fold())
            go_to_mix_wav_tunggal_cut_overlap()
            overlap.export(particle_overlap_name_export)
            go_to_project_dir()

            # EXPORT CSV
            csv_name_export = export_overlapped_csv(oe1, increment)
            go_to_metadata_dir()
            df_combined.to_csv(csv_name_export, header=False)
            go_to_project_dir()
            print('\tCsv exported as', Fore.LIGHTMAGENTA_EX, csv_name_export, Fore.WHITE)

            # EXPORT AUDIO
            overlayed = original_audio.overlay(particle_audio_df2, position=ae1_start*100)
            go_to_mix_dev()
            audio_name_export = export_overlapped_audio(oe1_ae, increment)
            overlayed.export(audio_name_export)
            print('\tWav exported as', Fore.LIGHTBLUE_EX, audio_name_export, Fore.WHITE)
            go_to_project_dir()

            # ADD HISTORY to dataframe
            row_history = np.array([
                oe1.get_foa(), oe2.get_foa(), oe1_ae.get__class(), particle1_name, oe2_ae.get__class(), particle2_name, audio_name_export,particle_overlap_name_export
            ])
            history_df = pd.DataFrame(row_history.reshape(1,-1))
            history = pd.concat([history, history_df])            # append to df

            # increment for each vars
            increment = increment + 1
    
    # EXPORT HISTORY
    history_name_export = export_history(oe1.get_csv_filename(), oe2.get_csv_filename())
    go_to_history_dev()
    history.to_csv(history_name_export, header=False, index=False)
    go_to_project_dir()

    # Notify the process is done
    print('History exported', Fore.LIGHTMAGENTA_EX, history_name_export, Fore.WHITE)        

# TODO: main
if __name__ == '__main__':
    global universal_counter_fold1
    universal_counter_fold1 = 1
    global universal_counter_fold2
    universal_counter_fold2 = 1
    global universal_counter_fold3
    universal_counter_fold3 = 1
    global universal_counter_fold4
    universal_counter_fold4 = 1
    global universal_counter_fold5
    universal_counter_fold5 = 1
    global universal_counter_fold6
    universal_counter_fold6 = 1

    global universal_counter_mix_fold1
    universal_counter_mix_fold1 = 1
    global universal_counter_mix_fold2
    universal_counter_mix_fold2 = 1
    global universal_counter_mix_fold3
    universal_counter_mix_fold3 = 1
    global universal_counter_mix_fold4
    universal_counter_mix_fold4 = 1
    global universal_counter_mix_fold5
    universal_counter_mix_fold5 = 1
    global universal_counter_mix_fold6
    universal_counter_mix_fold6 = 1
    
    folder_start = 1
    folder_end = 3

    clear_screen()

    all_files = get_all_files_in_metadata_dev(folder_start, folder_end)    # ! read all files

    all_objects = init_all_objects(all_files[0], export_audio=True, skip_confirm=True)    # ! init object from all files

    overlay_all_objects(all_objects, folder_start, all_files[1])    # ! overlay audio with the desired algorithm

    print(Fore.GREEN,'\nProgram is done running...',Fore.WHITE)