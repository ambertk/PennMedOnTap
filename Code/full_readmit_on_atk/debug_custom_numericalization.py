__author__ = 'nlsegerl'

from uphs_fields import *



gender_encoding = {
    'M':1,
    'F':2,
    'UNKNOWN':3
}


race_encoding = {
'WHITE':1,
'BLACK':2,
'None':3,
'UNKNOWN':4,
'ASIAN':5,
'OTHER':6,
'AM IND AK NATIVE':7,
'HI PAC ISLAND':8,
'(Empty)':9
}

hospice_encoding = {
'N' : 1, 'Y':2, 'None':3
}

marital_status_encoding = {
'M':1,  'S':2,  'None':3, 'UNKNOWN':4,  'W':5 , 'D':6,  'A':7, 'X':8, 'N':9, 'Y':10
}


from udf_installation import *


"""
numericalize all given string features in frame to integer features

returns a modified copy of the input frame

column names of new frame match those of incoming frame
"""

def numericalize_frame(ta, in_frame, frame_name,  overwrite = True):
    print "*** Numericalizing string features of frame " + in_frame.name
    print "*** Frame with numerical features: " + frame_name





    if (frame_name in ta.get_frame_names()):
        if (not overwrite):
            return ta.get_frame(frame_name)
        else:
            ta.drop_frames([frame_name])

    numericalized_frame = in_frame.copy(name = frame_name)

    add_udf_files(ta, [uphs_fields, 'debug_custom_numericalization.py'])

    target_cols = [RACE, GENDER, HOSPICE_FLAG , MARITAL_STATUS]
    target_schema = [ (col + "_INT", ta.int32) for col in target_cols]

    numericalized_frame.add_columns(lambda row:  [ race_encoding[row[RACE]], gender_encoding[row[GENDER]], hospice_encoding[row[HOSPICE_FLAG]], marital_status_encoding[row[MARITAL_STATUS]]], target_schema)
    numericalized_frame.drop_columns(target_cols)
    numericalized_frame.rename_columns( { col + "_INT": col for col in target_cols })
    return numericalized_frame

