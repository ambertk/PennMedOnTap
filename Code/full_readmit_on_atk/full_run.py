__author__ = 'nlsegerl'


"""
This script performs the following steps of the UPHS pipeline:

1. train/test split allocation per patient ID
2. ground truth labeling for the target function (R30 and R90 scores)
3. generation of cleaned features for Random Forest ingestion
4. generation of medical history table
5. preprocessing for LDA consumption

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
meds_frame_name = 'uphs_demo_per_visit_meds'
med_history_frame_name = 'uphs_demo_med_history'
lda_input_frame_name  = 'uphs_demo_lda_input'
meds_lda_topics_frame_name = 'uphs_demo_meds_lda_topics'
rf_input_frame_name = 'uphs_demo_rf_input'
rf_train_frame_name = 'uphs_demo_rf_train'
rf_test_frame_name  = 'uphs_demo_rf_test'
rf_base_model_name  = 'uphs_demo_base_rf_model'
rf_wlda_model_name  = 'uphs_demo_wlda_rf_model'

meds_lda_model_name = 'uphs_demo_meds_lda_model'
ta.connect()

import udf_installation
udf_installation.install_all_udf_files(ta)

overwrite_crossval_labels = False
overwrite_ground_truth = False
overwrite_basic_features = False
overwrite_med_visits = False
overwrite_med_history = False
overwrite_lda_preprocess = False
overwrite_numericalized_features = False
overwrite_joined_tables = True
overwrite_traintest = True
overwrite_model = True

print "\n\nGREETINGS HUMAN!!!\n"
print "initiating UPHS readmittance calculation on Intel TrustedAnalytics\n"

# create a table of patient IDs and their train/test labels

from cross_validation_labels import create_crossval_labeled_patids

print "Stage 1/10: Generate Table of Cross Validation Labels:  " + crossval_labeled_patids_frame_name

crossval_labeled_patids = create_crossval_labeled_patids(ta,
                                                         crossval_labeled_patids_frame_name,
                                                         in_path = inpatient_json_path,
                                                         overwrite = overwrite_crossval_labels)

print "Stage 2/10:  Generate Ground Truth Labels:  " + ground_truth_frame_name
from ground_truth import create_ground_truth
ground_truth =  create_ground_truth(ta, ground_truth_frame_name, inpatient_json_path, overwrite = overwrite_ground_truth)


print "Got ground truth for " + str(ground_truth.row_count) + " many rows"

print "Stage 3/10:  Generating and cleaning basic features: " + basic_features_frame_name
from basic_features import get_basic_features
basic_features  = get_basic_features(ta, basic_features_frame_name, inpatient_json_path, overwrite = overwrite_basic_features)

print "Got basic features for " + str(basic_features.row_count) + " many rows"


print "stage 4/10: Generating medical history features:  " + med_history_frame_name
from drug_frame import build_meds_frame, generate_med_history
meds_frame = build_meds_frame(ta, meds_frame_name, inpatient_json_path, overwrite = overwrite_med_visits)


meds_history = generate_med_history(ta, meds_frame, med_history_frame_name, overwrite = overwrite_med_history)


print "Stage 5/10: Preprocessing for LDA, producing frame: " + lda_input_frame_name
from drug_frame import preprocess_for_lda
lda_input = preprocess_for_lda(ta, meds_history, lda_input_frame_name, overwrite=overwrite_lda_preprocess)


from drug_frame import run_lda, get_features
num_topics = 20
lda_results = run_lda(ta, lda_input, meds_lda_model_name, num_topics)
doc_mixes = lda_results['topics_given_doc']
(meds_lda_feature_frame, topic_features) = get_features(ta, doc_mixes, feature_frame_name = 'uphs_demo_meds_lda_topics', topic_name = "topic", num_topics = num_topics)

print "Stage 6/10: Numericalizing string features"
from uphs_fields import *
from feature_encoding import  numericalize_frame
numericalized_basic_features = numericalize_frame(ta, basic_features, basic_features_frame_numericalized_name,
                                                  [RACE, GENDER, HOSPICE_FLAG , MARITAL_STATUS],
                                                  overwrite = overwrite_numericalized_features)

print "Stage 7/10: Creating input frames for random forest"
from prep_rf_input import  join_tables, create_test_table, create_train_table

rf_input = join_tables(ta, numericalized_basic_features, meds_lda_feature_frame,  crossval_labeled_patids, ground_truth, rf_input_frame_name, overwrite = overwrite_joined_tables)

rf_train = create_train_table(ta, rf_input, rf_train_frame_name, overwrite_traintest)
rf_test  = create_test_table(ta, rf_input, rf_test_frame_name, overwrite_traintest)



print "Stage 9/10: Run Random Forest and Evaluate results"


observation_columns = topic_features + [
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
