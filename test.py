import os

from go_to import go_to_metadata_dir, go_to_project_dir

go_to_metadata_dir()
for i in range(0,6):
    name = 'fold3_room1_mix' + '%03d' % i + '_ov1.csv'
    f = open(name, 'w')
    f.close()
go_to_project_dir()