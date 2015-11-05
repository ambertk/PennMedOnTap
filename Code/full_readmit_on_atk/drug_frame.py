__author__ = 'nlsegerl'

from uphs_fields import *
from derived_features import *
import uphs_loader as loader
from udf_installation import  *
from impute import impute_with_constants

import clean_drugs as drug_cleaner

# new column for combined patient and visit IDs

medlist_delimiter = '|'
history_delimiter = '*'

"""
Creates a frame keyed by PATID and VISID which contains
the cleaned drug orders for each visit in the column  COMBINED_MEDLIST
"""

def build_meds_frame(ta, frame_name, in_path, overwrite = True):

    print "*** CREATING DRUG HISTORY FRAME at " + frame_name
    if (frame_name in ta.get_frame_names()):
        if (not overwrite):
            return ta.get_frame(frame_name)
        else:
            ta.drop_frames([frame_name])

    add_udf_files(ta, [clean_drugs, derived_features, history_utilities, uphs_fields, uphs_schema])

    data_fields = [ PATID, VISID, ADM_DATE,  MED_ORDER_NAMEs, DISCHARGE_MED_ORDER_NAMEs ]
    data_frame = loader.load_frame(ta, in_path, frame_name, data_fields)

    print "Filtering out rows with missing or junk patient ids and/or visit ids"

    data_frame.filter(lambda row:  row[PATID] != None and row[VISID] != None and [PATID] != 'None' and row[VISID] != 'None')
    data_defaults = {MED_ORDER_NAMEs : "", DISCHARGE_MED_ORDER_NAMEs: ""}

    print "Imputing missing drug fields with empty lists"
    impute_with_constants(data_frame, data_defaults)


    data_frame.add_columns(lambda row: row[MED_ORDER_NAMEs] + ", " + row[DISCHARGE_MED_ORDER_NAMEs], (UNCLEAN_COMBINED_MEDLIST, str))
    data_frame.drop_columns([MED_ORDER_NAMEs, DISCHARGE_MED_ORDER_NAMEs])

    data_frame.add_columns(lambda row: drug_cleaner.to_clean_doc(row[UNCLEAN_COMBINED_MEDLIST], medlist_delimiter), (COMBINED_MEDLIST, str))
    data_frame.drop_columns([UNCLEAN_COMBINED_MEDLIST])

    return data_frame


"""
This return takes the cleaned medlists frame and produces the drug histories frame:

Drug history is the combined cleaned drug lists of all emergency visits 90 days prior to the current visit.

- records in the medlists frame are gathered into JSon records and placed in a new column called 'json_visit'
  (So we have a single "record" of the visit as a string that we can stuff into histories.)

- the jsonized visits are then grouped by patient IDs to form "patient histories"
     these are lists of jsonized visits, encoded as character delimited strings

- from these histories we can compute the previous 90 day drug history for each visit
"""

def generate_med_history(ta, in_frame, frame_name, overwrite = True):
    if (frame_name in ta.get_frame_names()):
        if (not overwrite):
            return ta.get_frame(frame_name)
        else:
            ta.drop_frames([frame_name])

    demo_test_drugs_per_visit_jsonized_name = frame_name + "__jsonized_temp"
    if (demo_test_drugs_per_visit_jsonized_name in ta.get_frame_names()):
        if (not overwrite):
            return ta.get_frame(demo_test_drugs_per_visit_jsonized_name)
        else:
            ta.drop_frames([demo_test_drugs_per_visit_jsonized_name])


    demo_test_drugs_per_visit_historized_name = frame_name + "__historized_temp"

    if (demo_test_drugs_per_visit_historized_name in ta.get_frame_names()):
        if (not overwrite):
            return ta.get_frame(demo_test_drugs_per_visit_historized_name)
        else:
            ta.drop_frames([demo_test_drugs_per_visit_historized_name])

    jsonized_visit = 'json_visit'
    import history_features
    from history_features import jsonize
    demo_test_drugs_per_visit_jsonized = jsonize(ta, in_frame,
                                                 demo_test_drugs_per_visit_jsonized_name,
                                                 jsonized_visit,
                                                 key_col_name = PATID)


    add_udf_files(ta, [clean_drugs, history_utilities, history_features,derived_features, historical_features_schema, uphs_fields])

    demo_test_drugs_per_visit_histories = history_features.historize(ta, demo_test_drugs_per_visit_jsonized, PATID,
                                                                     demo_test_drugs_per_visit_historized_name,
                                                                     jsonized_visit,
                                                                     delimiter = history_delimiter)


    demo_test_drug_histories = in_frame.join(demo_test_drugs_per_visit_histories, left_on = PATID, how = 'left', name = frame_name)

    from  history_utilities import inpat_med_lists_prior_to_admit, inpat_med_lists_prior_to_admit_schema
    demo_test_drug_histories.add_columns(lambda row: inpat_med_lists_prior_to_admit(row[ADM_DATE], 90,
                                            row[jsonized_visit], COMBINED_MEDLIST, history_delimiter), inpat_med_lists_prior_to_admit_schema)

    demo_test_drug_histories.drop_columns([jsonized_visit, COMBINED_MEDLIST, PATID+'_R'])


    return demo_test_drug_histories


"""
Transforms visit-to-druglist table into a visit-to-drug count table to ease ingestion by LDA.
Drug histories are expanded (so that there is one drug per row) and then counts are taken per visit, so that
in the final frame, there is a VISIT - DRUG - COUNT-OF-DRUG-IN-HISTORY form
"""

def preprocess_for_lda(ta, in_frame, frame_name, overwrite = True):

    print "*** PREPROCESSING DRUG HISTORIES FOR LDA INGESTION, CREATING " + frame_name
    if (frame_name in ta.get_frame_names()):
        if (not overwrite):
            return ta.get_frame(frame_name)
        else:
            ta.drop_frames([frame_name])

    lda_input = in_frame.copy()

    lda_input.add_columns(lambda row: row[PATID] + row[VISID], (EVENT_ID, str))

    lda_input.flatten_column(INPAT_HISTORICAL_MEDLIST, medlist_delimiter)

    lda_input = lda_input.group_by([EVENT_ID, PATID, VISID, INPAT_HISTORICAL_MEDLIST], ta.agg.count)
    lda_input_renamed = lda_input.copy(name = frame_name) # so damned annoying we can't give a name to the newly grouped frame!!!
    ta.drop_frames(lda_input) # so damned annoying... join lets us do it but not group_by... ugh
    return lda_input_renamed


"""
Run LDA-based topic modelling on the visit-drug count-in-history frame

return the LDA results dictionary object
"""

def run_lda(ta, in_frame, model_name, num_topics = 15):
    if model_name in ta.get_model_names():
        ta.drop_models(model_name)
    lda_model =  ta.LdaModel(name = model_name )
    print "Running LDA"
    dict = lda_model.train( in_frame, EVENT_ID, INPAT_HISTORICAL_MEDLIST , 'count',
                            num_topics = num_topics,
                            max_iterations=100)
    return dict

"""
Add topic-features to a frame from an LDA results dictionary.
"""
def get_features(ta, doc_results, feature_frame_name, topic_name = "topic", num_topics=15):
    if feature_frame_name in ta.get_frame_names():
        ta.drop_frames(feature_frame_name)
    feature_frame = doc_results.copy(name = feature_frame_name)
    topic_features_schema = map(lambda i: (topic_name + "_" + str(i), ta.float64), range(1, num_topics + 1))
    feature_frame.add_columns(lambda row: (row['topic_probabilities']), topic_features_schema)
    feature_frame.drop_columns(['topic_probabilities'])
    return (feature_frame, [ name for (name, type) in topic_features_schema])

