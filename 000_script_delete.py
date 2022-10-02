import os
from go_to import *

# go_to_mix_dev()
go_to_metadata_dir()
# go_to_history_dev()
# go_to_wav_tunggal_cut()
# go_to_mix_wav_tunggal_cut_overlap()

files = os.listdir()
for f in files:
    print(f)
    if 'ov2' in f:
        os.remove(f)