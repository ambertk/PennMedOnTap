__author__ = 'nlsegerl'

from ground_truth_utils import *

from uphs_loader import load_frame
import history_features

from filters import *
from udf_installation import *


"""
create_ground_truth_frame

Creates frame containing PATID, VISID, READMIT_30, READMIT_90 columns
stored with name frame_name,
data drawn from in_path

READMIT_30 is the 30-day emergency readmit flag, 1 if true, 0 if false
READMIT_90 is the 90-day emergency readmit, 1 if true, 0 if false


high level outline:

- basic visit information is pulled from JSon in an ATK dataframe and filtered for missing dates and IDs

- visit records are collapsed into individual JSon records (consisting of PATID, VISID, ADMIT_TYPE,
   ADM_DATE, DISCHARGE_DATE)

- these records are then "historized" - that is, converted into patient histories
  which is just all of the JSon visit records per patient gathered into a big '|' separated list-as-string
  (we do this because trustedanalytics does not yet support lists as a basic datatype_

- readmit scores are calculated by scanning over each of these gathered histories
  There is a rub here:
     histories are lists stored per patient ID
     readmit scores are per patient-visit compound ID --
    so we do an add columns that generates a 'list' of per visit readmit scores per patient and then flatten that out

"""

def create_ground_truth(ta, frame_name, in_path, overwrite = False):

    add_udf_files(ta, [uphs_fields, history_utilities,  ground_truth_utilities,  derived_features, filters])

    if (frame_name in ta.get_frame_names()):
        if (not overwrite):
            return ta.get_frame(frame_name)
        else:
            ta.drop_frames([frame_name])

    fields = [PATID, VISID, ADMIT_TYPE, ADM_DATE, DISCHARGE_DATE]

    base_frame_name =  '__' + frame_name + '_uphs_demo_visit_types'
    jsonized_frame_name = '__' + frame_name + '_jsonized_visits'
    json_col_name = 'visit_history'

    print "*** CREATE GROUND TRUTH FRAME AT FRAME: " + frame_name

    print "******  loading data from raw json"
    base_frame = load_frame(ta, in_path, base_frame_name, fields)

    print "****** filtering out bad rows with missing information"
    base_frame.filter(lambda row: patid_filter(row) and visid_filter(row) and adm_date_filter(row) and emergency_admit_filter(row))


    print "****** creating visit history atomic records"
    jsonized_frame = history_features.jsonize(ta, base_frame, jsonized_frame_name, json_col_name, key_col_name = PATID, overwrite = overwrite)

    print "****** collecting visit history"
    # historized_frame gets the output frame name since all subsequent changes are in-place and mutate the frame..
    # it will be the frame that goes out as the ground truth frame

    ground_truth_history_delimiter = '|'
    historized_frame = history_features.historize(ta, jsonized_frame, frame_name, json_col_name,
                                                  PATID, delimiter = ground_truth_history_delimiter)


    print "****** calculating READMIT_30 and READMIT_90 scores"

    LABELED_VISIT_JSON = 'LABELED_VISIT_JSON'
    # each patient gets a list of visits and their readmit scores
    historized_frame.add_columns(lambda row: per_visit_readmit_scores(row[json_col_name]), (LABELED_VISIT_JSON, str))

    historized_frame.drop_columns([json_col_name])

    # per patient list of visit/label readmit scores collapsed to per patient-visit readmit records
    historized_frame.flatten_column(LABELED_VISIT_JSON, delimiter = ground_truth_history_delimiter)

    print "******  placing READMIT_30 and READMIT_90 data into desired tabular format"
    # expanding json records per visit into multiple columns
    historized_frame.add_columns(lambda row: labeled_visit_to_columns(row[LABELED_VISIT_JSON]), labeled_visit_schema)
    historized_frame.drop_columns([LABELED_VISIT_JSON])

    ta.drop_frames([base_frame, jsonized_frame])

    return historized_frame

