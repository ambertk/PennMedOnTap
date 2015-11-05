#!/usr/bin/python2.7
import json

import uphs_schema as uphs
from udf_installation import *


fields = uphs.fields

"""
Load an trustedanalytics data frame from a JSon file using the UPHS cardiac data fields and schema.

ta: a connection to a trustedanalytics instance
in_path : path to the JSon files in UPHS cardiac format
frame_name: name of the new frame to be created
fields:   list of the fields to extract

resulting dataframe will have a column for each field requested, of the datatype specified in uphs_schema

If a frame with the requested name already exists, it will be dropped to create the new frame!
"""
def load_frame(ta, in_path, frame_name, fields):

    # uphs_schama_installer.install(ta, project_root)

    schema = uphs.get_schema(fields)

    print "Loading UPHS patient data from HDFS path " + in_path + " into data frame " + frame_name
    print "Requested fields: "
    print ', '.join(fields)
    print "Resulting Schema: "
    print ''.join('{}{}'.format(key, val) for key, val in dict(schema).items())

    # Create ATK json object...
    input_json_file = ta.JsonFile(in_path)

    # Create ATK frames...


    if frame_name in ta.get_frame_names():
        ta.drop_frames(frame_name)
    data_frame = ta.Frame(input_json_file, name=frame_name)

    # add_columns...

    """

    """
    def extract_github_json(row):
        my_json = json.loads(row[0])
        out_list = map((lambda f: my_json[f] if f in my_json else None), fields)
        return out_list


    def clean_type(val, type):
        try:
            return type(val)
        except:
            return None

    add_udf_files(ta, [uphs_fields, uphs_schema, uphs_loader])

    schema_types = [type for (name, type) in schema ]

    data_frame.add_columns(
        lambda row: map(lambda (val, type): clean_type(val, type),  zip(extract_github_json(row), schema_types)),
        schema
    )

    # Drop the data_lines column...
    data_frame.drop_columns('data_lines')
    return data_frame


