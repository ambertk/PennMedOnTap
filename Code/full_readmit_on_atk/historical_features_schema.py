from history_feature_names import *

derived_feature_schema = [
    (ER_VISIT_COUNT, ta.int32),
    (OUTPATIENT_VISIT_COUNT, ta.int32),
    (HISTORICAL_INPAT_MEDLIST, str),
    (HISTORICAL_OUTPAT_MEDLIST, str)
]


derived_feature_schema_dictionary = dict(derived_feature_schema)
fields = derived_feature_schema_dictionary.keys()

# checks that a given field name is a valid UPHS field name

def check_field(f):
    if not f in fields:
        print "Bad field name : " + f + "\n"
        return False
    else:
        return True

def check_fields(in_fields):
    return all(check_field(f) for f in in_fields)

def get_schema(in_fields):
    if (check_fields(in_fields)):
        return map(lambda field: (field, derived_feature_schema_dictionary[field]), in_fields)
    else:
        print "Bad field name, no schema produced."
        return []
