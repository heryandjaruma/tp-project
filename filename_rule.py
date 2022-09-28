def export_overlapped_audio(oe1_ae, oe2_ae, increment_original, increment_particle):
    # return "_".join([oe1_ae.get_fold(), oe1_ae.get_room(), oe1_ae.get_mix(), 'ov2', oe2_ae.get_fold(), '%03d_%03d' % (increment_original, increment_particle)]) + '.wav'

    return "_".join([oe1_ae.get_fold(), oe1_ae.get_room(), oe1_ae.get_mix(), 'ov2', oe2_ae.get_fold(), oe2_ae.get_room(), oe2_ae.get_mix(), '%03d_%03d' % (increment_original, increment_particle)]) + '.wav'
    # e.g. : fold1_room1_mix001_ov2_001_001.wav

def export_overlapped_csv(oe1, oe2, increment_original, increment_particle):
    # return "_".join([oe1.get_fold(), oe1.get_room(), oe1.get_mix(), 'ov2', oe2.get_fold(), '%03d_%03d' % (increment_original, increment_particle)]) + '.wav'

    return "_".join([oe1.get_fold(), oe1.get_room(), oe1.get_mix(), 'ov2', oe2.get_fold(), oe2.get_room(), oe2.get_mix(), '%03d_%03d' % (increment_original, increment_particle)]) + '.csv'
    # return oe1.get_csv_filename().replace('ov1', '%s_ov2_%03d_%03d' % (oe2.get_fold(), increment_original, increment_particle))
    # e.g. : fold1_room1_mix001_ov2_001_001.csv

def export_history(oe1_filename, oe2_filename):
    return oe1_filename[:-4] + '_OV_' + oe2_filename[:-4] + '.csv'
    # e.g. : fold1_room1_mix001_ov1_OVERLAP_fold2_room1_mix001_ov1.csv

def export_particle_audio(fold, room, mix, entity_num):
    return "_".join([fold, room, mix,'class%02d' % int(entity_num + 1)]) + '.wav'