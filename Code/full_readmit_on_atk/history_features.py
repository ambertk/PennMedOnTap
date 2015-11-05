from uphs_fields import  *


"""
jsonize

Compress rows of patient data into json records keyed by patient id (or some other key).

Creates a copy of incoming frame. Does not modify the input frame.

EXAMPLE:

in frame has schema: PATID, ADMIT_DATE, DISCHARGE_DATE, ADMIT_TYPE
key_col_name is PATID
jscon_col_name is JSONIZED_VISIT

then...

new frame  has schema PATID, JSONIZED_VISIT
and each entry in th JSONIZED_VISIT row is a json-object-as-string with fields
   PATID, ADMIT_DATE, DISCHARGE_DATE, ADMIT_TYPE
"""
def jsonize(ta, in_frame, new_frame_name, json_col_name, key_col_name = PATID, overwrite = True):
    print "Compressing rows of " + in_frame.name + " into json records keyed by " + key_col_name
    print "name of new frame: " + new_frame_name
    print "name of json column in new frame: " + json_col_name

    import json
    if (new_frame_name in ta.get_frame_names()):
        ta.drop_frames(new_frame_name)

    print "Copying the input frame"
    new_frame = in_frame.copy(name=new_frame_name)
    print "Adding jsonized rows as column " + json_col_name


    new_frame.add_columns(lambda row: json.dumps(dict(row)), (json_col_name, str))
    print "Dropping unused columns from " + new_frame_name
    new_frame.drop_columns([col_name for (col_name, type) in new_frame.schema
                            if col_name != json_col_name and col_name != key_col_name])
    return new_frame


"""
historize

Creates history field by combining jsonized records that belong to same key_column into a list (as a
character separated list).
"""
def historize(ta, in_frame, new_frame_name, record_col_name,  key_col_name, delimiter , overwrite = True):
    print "Collecting patient records in column " + record_col_name + " by key " + key_col_name
    print "History delimiter == " + delimiter
    print "name of new frame: " + new_frame_name

    print "Copying the incoming frame..."
    if (new_frame_name in ta.get_frame_names()):
        ta.drop_frames(new_frame_name)
    new_frame = in_frame.copy(name = new_frame_name)
    new_frame.unflatten_column(key_col_name, delimiter)
    return new_frame


