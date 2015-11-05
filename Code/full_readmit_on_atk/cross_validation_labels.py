__author__ = 'nlsegerl'



from uphs_fields import *
from uphs_loader import load_frame
from derived_features import  *
from filters import patid_filter
from udf_installation import  *


"""
Label patient IDs by train/test split so we can perform cross validation based on the patient population.
The table produced has two columns: PATID and CROSS_VALIDATION_CLASS
"""



def create_crossval_labeled_patids(ta, frame_name, in_path, overwrite = True):
    fields = [PATID]

    print "****** Assigning train/test labels for cross validation... loading data"
    if (frame_name in ta.get_frame_names()):
        if (not overwrite):
            return ta.get_frame(frame_name)
        else:
            ta.drop_frames(frame_name)


    frame = load_frame(ta, in_path, frame_name, fields)

    print "****** Assigning train/test labels for cross validation... identiyfing patient population"
    add_udf_files(ta, [uphs_fields, filters])
    frame.filter(lambda row: patid_filter(row))
    frame.drop_duplicates()

    print "****** Assigning train/test labels for cross validation... assigning labels"
    frame.assign_sample(sample_percentages = [0.9, 0.1],
                        sample_labels = [TRAIN_LABEL, TEST_LABEL],
                        random_seed = 1776,
                        output_column = CROSS_VALIDATION_CLASS)

    return frame
