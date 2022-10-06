# def export_overlapped_audio(oe1_ae, increment):                                                                     #! export to mix_dev
#     return "_".join([oe1_ae.get_fold(), oe1_ae.get_room(), oe1_ae.get_mix(), 'ov2', '%03d' % (increment)]) + '.wav'
def export_overlapped_audio(oe1_ae, increment):                                                                     #! export to mix_dev
    return "_".join([oe1_ae.get_fold(), oe1_ae.get_room(), 'mix%03d' % (increment), 'ov2']) + '.wav'

def export_overlapped_csv(oe1, increment):                                                                          #! export to metadata_dev
    return "_".join([oe1.get_fold(), oe1.get_room(), 'mix%03d' % (increment), 'ov2']) + '.csv'
# def export_overlapped_csv(oe1, increment):                                                                          #! export to metadata_dev
#     return "_".join([oe1.get_fold(), oe1.get_room(), oe1.get_mix(), 'ov2', '%03d' % (increment)]) + '.csv'

def export_history(oe1_filename, oe2_filename):                                                                     #! export to history_dev
    return oe1_filename[:-4] + '_OVERLAP_' + oe2_filename[:-4] + '.csv'

def export_particle_audio(fold, room, mix, ov, _class):                                                             #! export to wav_tunggal
    return "_".join([str(fold), str(room), str(mix), str(ov),str(_class)]) + '.wav'

def export_particle_label_only(fold, room, mix, _class, counter):                                                   #! export to wav_tunggal_cut
    return "_".join([str(fold), str(room), str(mix), str(_class), '%03d' % (counter)]) + '.wav'

def export_particle_label_overlap(fold, room, mix, _class1, _class2, counter):                                      #! export mix_wav_tunggal_cut
    return "_".join([str(fold), str(room), str(mix),str(_class1), str(_class2), '%03d' % (counter)]) + '.wav'