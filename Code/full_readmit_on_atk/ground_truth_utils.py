__author__ = 'nlsegerl'


from uphs_fields import *
import trustedanalytics as ta

"""
per_visit_readmit_scores

Takes a list of json visit records (as a character separated string), containing VISID, ADM_DATE, DISCHARGE_DATE,
and produces list of json visit records (as a character separated string), containing VISID, READMIT_30 and READMIT_90

"""
def per_visit_readmit_scores(json_records_as_charsepstring, delimiter ='|'):
    import json
    from history_utilities import char_sep_string_to_list, list_to_char_sep_string, get_datetime_from_atk_encoding


    json_records_as_listofstrings = char_sep_string_to_list(json_records_as_charsepstring, delimiter = delimiter)
    json_records = map(json.loads, json_records_as_listofstrings)

    sorted_json_records = sorted(json_records, key=lambda r: get_datetime_from_atk_encoding(r[ADM_DATE]))

    list_of_json_label_records = []

    for i in range(0, len(sorted_json_records)):
        visit = sorted_json_records[i]
        visid = visit[VISID]
        if (i < len(sorted_json_records) - 1):
            next_visit = sorted_json_records[i+1]
            discharge = get_datetime_from_atk_encoding(visit[DISCHARGE_DATE])
            next_admit = get_datetime_from_atk_encoding(next_visit[ADM_DATE])
            r30  = 1 if dates_within_window(discharge,next_admit, window_in_days=30) else 0
            r90  = 1 if dates_within_window(discharge,next_admit, window_in_days=90) else 0
        else:  # at this point, i = len(sorted_json_records) -1 , ie. it is the final record
            r30 = 0
            r90 = 0
        list_of_json_label_records += [create_json_label_rec(visid,r30, r90)]

    return list_to_char_sep_string(list_of_json_label_records, delimiter)


"""
dates_with_window

True iff datetime object t1 occurs before datetime object t0 plus 90 days
"""
def dates_within_window(t0, t1, window_in_days):
    # this is debug code
    td_days = divmod((t1-t0).days, 60)[-1]
    return td_days <= window_in_days
    # return  ((t1 - t0).days <= window_in_days)

"""
create_json_label_rec

Create json record of VISID, READMIT_30, READMIT_90 dictionary from input
"""
def create_json_label_rec(visid, r30, r90):
    import json
    dict = {VISID : visid, READMIT_30 : r30, READMIT_90 : r90}
    return json.dumps(dict)


"""
Takes a string-encoded json record of a visit -
with fields VISID, READMIT_30 and READMIT_90 and
emits a list [VISID, READMIT_30, READMIT_90]

A helper to generate columns with labels.
"""
def labeled_visit_to_columns(visit):
    import json
    jrec = json.loads(visit)
    visid = jrec[VISID]
    r30 = jrec[READMIT_30]
    r90 = jrec[READMIT_90]
    return [visid, r30, r90]


# NLS TODO:  don't we have all this information in some kind of get_schema function?
labeled_visit_schema =  [(VISID, str), (READMIT_30, ta.int32), (READMIT_90, ta.int32)]