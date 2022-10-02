import os

path_to_project_fold = r'D:\TPProject\mainv4'

def go_to_project_dir():
    os.path.dirname(path_to_project_fold)
def go_to_metadata_dir():
    os.chdir(path_to_project_fold+r'\metadata_dev')
def go_to_foa_dir():
    os.chdir(path_to_project_fold+r'\foa_dev')
def go_to_audio_entities_dev():
    os.chdir(path_to_project_fold+r'\wav_tunggal')
def go_to_mix_dev():
    os.chdir(path_to_project_fold+r'\mix_dev')
def go_to_history_dev():
    os.chdir(path_to_project_fold+r'\history_dev')
def go_to_wav_tunggal_cut():
    os.chdir(path_to_project_fold+r'\wav_tunggal_cut')
def go_to_mix_wav_tunggal_cut_overlap():
    os.chdir(path_to_project_fold+r'\mix_wav_tunggal_cut')