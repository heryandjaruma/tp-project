def export_overlapped_audio(oe1_ae, increment):
    return "_".join([oe1_ae.get_fold(), oe1_ae.get_room(), oe1_ae.get_mix(), 'ov2', '%03d' % (increment)]) + '.wav'
    # e.g. : fold1_room1_mix001_ov2_001_001.wav

def export_overlapped_csv(oe1, increment):
    return "_".join([oe1.get_fold(), oe1.get_room(), oe1.get_mix(), 'ov2', '%03d' % (increment)]) + '.csv'
    # e.g. : fold1_room1_mix001_ov2_001_001.csv

def export_history(oe1_filename, oe2_filename):
    return oe1_filename[:-4] + '_OVERLAP_' + oe2_filename[:-4] + '.csv'
    # e.g. : fold1_room1_mix001_ov1_OVERLAP_fold2_room1_mix001_ov1.csv

def export_particle_audio(fold, room, mix, ov, _class):
    # return "_".join([fold, room, mix,'class%02d' % int(entity_num + 1)]) + '.wav'
    return "_".join([str(fold), str(room), str(mix), str(ov),str(_class)]) + '.wav'

def export_particle_label_only(fold, room, mix, _class, increment):  #! export wav_tunggal_cut
    return "_".join([str(fold), str(room), str(mix), str(_class), '%03d' % (increment)]) + '.wav'

def export_particle_label_overlap(fold, room, mix, _class1, _class2, increment):    #! export mix_wav_tunggal_cut
    return "_".join([str(fold), str(room), str(mix),str(_class1), str(_class2), '%03d' % (increment)]) + '.wav'