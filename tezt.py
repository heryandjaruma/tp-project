from go_to import *

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

go_to_wav_tunggal_cut()
print(get_increment_number_label_only(1))
go_to_project_dir()

go_to_mix_wav_tunggal_cut_overlap()
print(get_increment_number_label_overlap(2))