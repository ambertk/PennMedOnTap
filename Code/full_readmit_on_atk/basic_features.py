__author__ = 'the coder formerly known as nlsegerl'

"""
Load the base model features for the PennMed cardiac readmit analysis.

Missing values are imputed with default values.
"""
from impute import impute_with_constants
from filters import *
import uphs_loader as loader
from udf_installation import *

# columns used in the baseline model are hardwired... we should parameterize these at the top level
# so we can run different basline models more simply

data_columns = [PATID,
                VISID,
                SEVERITY_ILLNESS_INDEX,
                HEIGHT_INCHES,
                WEIGHT_LBS,
                CEQI_READMIT_IS_READMIT_UNPL,
                RISK_MORTALITY_INDEX,
                DEATH_FLAG,
                AGE,
                GENDER,
                ARITHMETIC_LOS,
                HOSPICE_FLAG,
                CEQI_READMIT_DAYS_FROM_PREV,
                RACE,
                MARITAL_STATUS,
                CEQI_READMIT_IS_READMIT ]


default_values = {SEVERITY_ILLNESS_INDEX : 0, HEIGHT_INCHES: 66.0, WEIGHT_LBS: 150.0,
                  CEQI_READMIT_IS_READMIT_UNPL: 0, RISK_MORTALITY_INDEX : 0.0,
                  DEATH_FLAG: 0.0, AGE: 60, GENDER: 'UNKNOWN', ARITHMETIC_LOS : '0.0',
                  HOSPICE_FLAG: 'UNKNOWN', CEQI_READMIT_DAYS_FROM_PREV: 10000.0,
                  RACE: 'UNKNOWN', MARITAL_STATUS: 'UNKNOWN', CEQI_READMIT_IS_READMIT : 0}




def get_basic_features(ta, frame_name, in_path, overwrite = True):

    if (frame_name in ta.get_frame_names()):
        if (not overwrite):
            return ta.get_frame(frame_name)
        else:
            ta.drop_frames(frame_name)

    frame = loader.load_frame(ta, in_path, frame_name, data_columns)

    add_udf_files(ta, [uphs_fields, filters])

    frame.filter(lambda row: patid_filter(row) and visid_filter(row))

    impute_with_constants(frame, default_values)

    return frame

