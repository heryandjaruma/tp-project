import os
from env import *

def go_to_project_dir():
    os.path.dirname(path_to_project_fold)
def go_to_metadata_dir():
    os.chdir(path_to_project_fold+r'\metadata_dev')
def go_to_foa_dir():
    os.chdir(path_to_project_fold+r'\foa_dev')
def go_to_audio_entities_dev():
    os.chdir(path_to_project_fold+r'\audio_entity_dev')
def go_to_mix_dev():
    os.chdir(path_to_project_fold+r'\mix_dev')