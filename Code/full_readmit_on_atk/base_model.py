__author__ = 'nlsegerl'


"""
This script performs the following steps of the UPHS pipeline:

1. train/test split allocation per patient ID
2. ground truth labeling for the target function (R30 and R90 scores)
3. generation of cleaned features for Random Forest ingestion
4. numericalization of string categoricals for RF consumption
5. creation of input frames for random forest (join of train/test splits and ground truth labels into cleaned features)
6. build and evaluate a random forest model

"""


import trustedanalytics as ta

# where the inpatient data from UPHS sits on HDFS... ie. the  datasource for this workflow
inpatient_json_path = "data/UPHS/inpat/"
#inpatient_json_path = "data/UPHS/inpat_small/"

# The names of the frames used during feature engineering and model evaluation in the UPHS demo.

crossval_labeled_patids_frame_name = 'uphs_demo_crossval_labels'
ground_truth_frame_name = 'uphs_demo_ground_truth'
basic_features_frame_name = 'uphs_demo_basic_features'
basic_features_frame_numericalized_name = 'uphs_demo_basic_features_numericalized'

rf_input_frame_name = 'uphs_demo_rf_input'
rf_train_frame_name = 'uphs_demo_rf_train'
rf_test_frame_name  = 'uphs_demo_rf_test'
rf_base_model_name  = 'uphs_demo_base_rf_model_3'
rf_wlda_model_name  = 'uphs_demo_wlda_rf_model_3'

meds_lda_model_name = 'uphs_demo_meds_lda_model_2'
ta.connect()

import udf_installation
udf_installation.install_all_udf_files(ta)

overwrite_crossval_labels = False
overwrite_ground_truth = False
overwrite_basic_features = False
overwrite_numericalized_features = False
overwrite_joined_tables = True
overwrite_traintest = True
overwrite_model = True

print "\n\nGREETINGS HUMAN!!!\n"
print "initiating UPHS readmittance calculation on Intel TrustedAnalytics\n"

# create a table of patient IDs and their train/test labels

from cross_validation_labels import create_crossval_labeled_patids

print "Stage 1/6: Generate Table of Cross Validation Labels:  " + crossval_labeled_patids_frame_name

crossval_labeled_patids = create_crossval_labeled_patids(ta,
                                                         crossval_labeled_patids_frame_name,
                                                         in_path = inpatient_json_path,
                                                         overwrite = overwrite_crossval_labels)

print "Stage 2/6:  Generate Ground Truth Labels:  " + ground_truth_frame_name
from ground_truth import create_ground_truth
ground_truth =  create_ground_truth(ta, ground_truth_frame_name, inpatient_json_path, overwrite = overwrite_ground_truth)


print "Got ground truth for " + str(ground_truth.row_count) + " many rows"

print "Stage 3/6:  Generating and cleaning basic features: " + basic_features_frame_name
from basic_features import get_basic_features
basic_features  = get_basic_features(ta, basic_features_frame_name, inpatient_json_path, overwrite = overwrite_basic_features)

print "Got basic features for " + str(basic_features.row_count) + " many rows"


print "Stage 4/6: Numericalizing string features"
from uphs_fields import *
from feature_encoding import  numericalize_frame
numericalized_basic_features = numericalize_frame(ta, basic_features, basic_features_frame_numericalized_name,
                                                  [RACE, GENDER, HOSPICE_FLAG , MARITAL_STATUS],
                                                  overwrite = overwrite_numericalized_features)

print "Stage 5/6: Creating input frames for random forest"
from prep_rf_input import  join_tables, create_test_table, create_train_table

rf_input = join_tables(ta, numericalized_basic_features, None, crossval_labeled_patids, ground_truth, rf_input_frame_name, overwrite = overwrite_joined_tables)

rf_train = create_train_table(ta, rf_input, rf_train_frame_name, overwrite_traintest)
rf_test  = create_test_table(ta, rf_input, rf_test_frame_name, overwrite_traintest)


print "Stage 6/6: Run Random Forest and evaluate results"



observation_columns = [
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
    CEQI_READMIT_IS_READMIT]

from train_eval_model import  build_eval_model


build_eval_model(ta, rf_base_model_name, rf_train, rf_test, READMIT_30, observation_columns, overwrite = overwrite_model)
