import os
from go_to import go_to_metadata_dir, go_to_mix_dev

# go_to_mix_dev()
# go_to_metadata_dir()

files = os.listdir()
for f in files:
    print(f)
    if 'ov2' in f:
        os.remove(f)