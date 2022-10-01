def export_overlapped_audio(oe1_ae, increment):
    return "_".join([oe1_ae.get_fold(), oe1_ae.get_room(), oe1_ae.get_mix(), 'ov2', '%03d' % (increment)]) + '.wav'
    # e.g. : fold1_room1_mix001_ov2_001_001.wav

def export_overlapped_csv(oe1, increment):
    return "_".join([oe1.get_fold(), oe1.get_room(), oe1.get_mix(), 'ov2', '%03d' % (increment)]) + '.csv'
    # e.g. : fold1_room1_mix001_ov2_001_001.csv

def export_history(oe1_filename, oe2_filename):
    return oe1_filename[:-4] + '_ov2_' + oe2_filename[:-4] + '.csv'
    # e.g. : fold1_room1_mix001_ov1_OVERLAP_fold2_room1_mix001_ov1.csv

def export_particle_audio(fold, room, mix, entity_num):
    return "_".join([fold, room, mix,'class%02d' % int(entity_num + 1)]) + '.wav'

def export_particle_label_only(fold, room, mix, label_utama):
    return "_".join([str(fold), str(room), str(mix), str(label_utama)]) + '.wav'

def export_particle_label_overlap(fold, room, mix, label_utama, label_kedua):
    return "_".join([str(fold), str(room), str(mix), str(label_utama), str(label_kedua)]) + '.wav'