__author__ = 'nlsegerl'


import datetime
from uphs_fields import *
from derived_features import *

"""
first some basic time utilities
"""
def get_datetime_from_atk_encoding(date_in):
    timestamp = int(date_in.strip(   '{'    ).strip('}').split(':')[1]) / 1000
    return datetime.datetime.fromtimestamp(timestamp)

def length_of_stay_in_days(admit_date_atk, discharge_date_atk):
    admit_date = get_datetime_from_atk_encoding(admit_date_atk)
    discharge_date = get_datetime_from_atk_encoding(discharge_date_atk)
    time_delta = discharge_date - admit_date
    return time_delta.days


import json
# get admission date-time from UPHS medical visit json record, divides by 1000 to convert from milliseconds
# these work with json records, not rows!!!
# big assumption: the event HAS an admit date in its json
def get_admit_date(event_json):

    atk_encoded_date = event_json['ADM_DATE']
    return get_datetime_from_atk_encoding(atk_encoded_date)


# get discharge date-time from UPHS medical visit json record, divides by 1000 to convert from milliseconds
# big assumption: the event HAS a discharge date in its json
def get_discharge_date(event_json):
    weird_string_encoded_date = event_json['DISCHARGE_DATE']
    timestamp = int(weird_string_encoded_date.strip('{').strip('}').split(':')[1])
    return datetime.datetime.fromtimestamp(timestamp/1000)


"""
the events are json objects in a list
"""
def events_admitting_in_range(json_events, start, end):

    def f(json_event):
        date = get_admit_date(json_event)
        return date < end and start <= date
    return filter(f, json_events)


# kludgy ATK workarounds here
# right now ATK does not support lists of strings (in particular, lists of json objects) as primitive datatypes
# furthermore, the flatten/unflatter operations do not generate JSon sequences, but character separated strings

def char_sep_string_to_list(char_sep_string, delimiter = '|'):
    if char_sep_string == None:
        return []
    else:
        return char_sep_string.split(delimiter)

def list_to_char_sep_string(list, delimiter = '|'):
    return delimiter.join(list)

"""
get the combined drug fields for the ninety days previous to this visit
"""

def get_string_field(json_object, field):
    if (field in json_object):
        val = json_object[field]
        if (val == None):
            return ""
        else:
            return json_object[field]
    else:
        return ""


# window is the integer number of  DAYS
def inpat_med_lists_prior_to_admit(admit_date_atk, window,  inpat_history, meds_field, history_delimiter = '|'):

    if admit_date_atk == None:
        return ""

    end = get_datetime_from_atk_encoding(admit_date_atk)
    start = end - datetime.timedelta(days = window)


    import json
    inpat_json_events = filter(lambda event: ADM_DATE in event, map(json.loads, char_sep_string_to_list(inpat_history, delimiter=history_delimiter)))

    in_visits = events_admitting_in_range(inpat_json_events, start, end)


    from clean_drugs import to_clean_doc

    if (in_visits == []):
        return ""
    else:
        med_list =  ' '.join(map(lambda event: get_string_field(event, MED_ORDER_NAMEs) + get_string_field(event, meds_field), in_visits))
        return to_clean_doc(med_list)



inpat_med_lists_prior_to_admit_schema = (INPAT_HISTORICAL_MEDLIST, str)

