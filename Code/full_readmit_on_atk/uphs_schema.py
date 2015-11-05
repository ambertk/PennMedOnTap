"""
Utilities and definitions for managing the schema and datatypes of fields from the UPHS cardiac project.
"""

from uphs_fields import *

import trustedanalytics as ta



"""
full_schema

list of (field_name, datatype in trustedanalytics) pairs
"""

full_schema = 	[
    (ADMITTING_CCS_LVL_1_LABELs, str),
	(ADMITTING_CCS_LVL_2_LABELs, str),
	(ADMITTING_CCS_LVL_3_LABELs, str),
	(ADMITTING_CCS_LVL_4_LABELs, str),
	(ADMITTING_DIAG_CCS_LVL_1_LABELs, str),
	(ADMITTING_DIAG_CCS_LVL_2_LABELs, str),
	(ADMITTING_DIAG_CCS_LVL_3_LABELs, str),
	(ADMITTING_DIAG_CCS_LVL_4_LABELs, str),
	(ADMITTING_DIAG_CODEs, str),
	(ADMITTING_DIAG_DESCs, str),
	(ADMIT_REASONs, str),
	(ADMIT_RISK_MORTALITY_INDEX, str),
	(ADMIT_SERVICE_CODE, str),
	(ADMIT_SERVICE_DESCRIPTION, str),
	(ADMIT_SERVICE_GROUP, str),
	(ADMIT_SEVERITY_ILLNESS_INDEX, str),
	(ADMIT_SOURCE, str),
	(ADMIT_SOURCE_MEDVIEW, str),
	(ADMIT_TYPE, str),
	(ADM_DATE, str),
	(AGE, ta.int32),
	(ARITHMETIC_LOS, ta.float32),
	(CCS_LVL_1_LABELs, str),
	(CCS_LVL_2_LABELs, str),
	(CCS_LVL_3_LABELs, str),
	(CCS_LVL_4_LABELs, str),
	(CEQI_READMIT_DAYS_FROM_PREV, ta.float32),
	(CEQI_READMIT_IS_READMIT, ta.int32),
	(CEQI_READMIT_IS_READMIT_UNPL, ta.int32),
	(CEQI_READMIT_WILL_READMIT, ta.int32),
	(CEQI_READMIT_WILL_READMIT_UNPL,ta.int32),
	(COMORBIDITY_CCS_LVL_1_LABELs, str),
	(COMORBIDITY_CCS_LVL_2_LABELs, str),
	(COMORBIDITY_CCS_LVL_3_LABELs, str),
	(COMORBIDITY_CCS_LVL_4_LABELs, str),
	(COMORBIDITY_DIAG_CCS_LVL_1_LABELs, str),
	(COMORBIDITY_DIAG_CCS_LVL_2_LABELs, str),
	(COMORBIDITY_DIAG_CCS_LVL_3_LABELs, str),
	(COMORBIDITY_DIAG_CCS_LVL_4_LABELs, str),
	(COMORBIDITY_DIAG_CODEs, str),
	(COMORBIDITY_DIAG_DESCs, str),
	(Clinstream_Source, str),
	(DEATH_FLAG, ta.float32),
	(DEPARTMENTs, str),
	(DIAG_CCS_LVL_1_LABELs, str),
	(DIAG_CCS_LVL_2_LABELs, str),
	(DIAG_CCS_LVL_3_LABELs, str),
	(DIAG_CCS_LVL_4_LABELs, str),
	(DIAG_CODEs, str),
	(DIAG_DESCs, str),
	(DISCHARGE_DATE, str),
	(DISCHARGE_MED_ORDER_NAMEs, str),
	(DISCHARGE_STATUS, str),
	(DRG_COST_THRESHOLD, str),
	(DRG_OUTLIER_STATUS, str),
	(DRG_POST_ACUTE_YN, str),
	(DRG_SPECIAL_PAY_YN, str),
	(DRG_TYPE, str),
	(DRG_WEIGHT, str),
	(EMERGENCY_YN, str),
	(ENC_TYPE_CODE, str),
	(ENC_TYPE_DESCRIPTION, str),
	(FC_MASTER_DESCRIPTION, str),
	(FINAL_CCS_LVL_1_LABELs, str),
	(FINAL_CCS_LVL_2_LABELs, str),
	(FINAL_CCS_LVL_3_LABELs, str),
	(FINAL_CCS_LVL_4_LABELs, str),
	(FINAL_DIAG_CCS_LVL_1_LABELs, str),
	(FINAL_DIAG_CCS_LVL_2_LABELs, str),
	(FINAL_DIAG_CCS_LVL_3_LABELs, str),
	(FINAL_DIAG_CCS_LVL_4_LABELs, str),
	(FINAL_DIAG_CODEs, str),
	(FINAL_DIAG_DESCs, str),
	(GENDER, str),
	(GEOMETRIC_LOS, str),
	(HEIGHT_INCHES, ta.float32),
	(HOSPICE_FLAG, str),
	(HOSPITALs, str),
	(LOCATION, str),
	(LOS, str),
	(LOS_NUM, str),
	(Lab_obs_type_count, str),
	(Lab_startTime, str),
	(Lab_stats, str),
	(Lab_stopTime, str),
	(LastTSDate, str),
	(LastUpdateSource, str),
	(MARITAL_STATUS, str),
	(MDC, str),
	(MED_ORDER_NAMEs, str),
	(MED_ORDER_TYPE_DESCRIPTIONs, str),
	(MSDRG, str),
	(MSDRG_DESC, str),
	(ORDER_GROUPs, str),
	(ORDER_NAMEs, str),
	(ORDER_SET_NAMEs, str),
	(ORDER_SOURCE_CODEs, str),
	(ORDER_TYPE_DESCRIPTIONs, str),
	(PATID, str),
	(PATIENT_CLASS, str),
	(PDS_SOURCE, str),
	(PRIMARY_CCS_LVL_1_LABELs, str),
	(PRIMARY_CCS_LVL_2_LABELs, str),
	(PRIMARY_CCS_LVL_3_LABELs, str),
	(PRIMARY_CCS_LVL_4_LABELs, str),
	(PRIMARY_DIAG_CCS_LVL_1_LABELs, str),
	(PRIMARY_DIAG_CCS_LVL_2_LABELs, str),
	(PRIMARY_DIAG_CCS_LVL_3_LABELs, str),
	(PRIMARY_DIAG_CCS_LVL_4_LABELs, str),
	(PRIMARY_DIAG_CODEs, str),
	(PRIMARY_DIAG_DESCs, str),
	(PRIMARY_PROC_CCS_LVL_1_LABELs, str),
	(PRIMARY_PROC_CCS_LVL_2_LABELs, str),
	(PRIMARY_PROC_CCS_LVL_3_LABELs, str),
	(PRIMARY_PROC_CODEs, str),
	(PRIMARY_PROC_DESCs, str),
	(PROC_CCS_LVL_1_LABELs, str),
	(PROC_CCS_LVL_2_LABELs, str),
	(PROC_CCS_LVL_3_LABELs, str),
	(PROC_CODEs, str),
	(PROC_DESCs, str),
	(RACE, str),
	(REHAB_ASSESSMENT_YN, str),
	(RISK_MORTALITY_INDEX, ta.float32),
	(ROM, str),
	(SERVICE_CODE, str),
	(SERVICE_DESCRIPTION, str),
	(SERVICE_GROUP, str),
	(SERVICEs, str),
	(SEVERITY_ILLNESS_INDEX, ta.int32),
	(ServiceName, str),
	(UNIT, str),
	(UNIT_MASTER_CARE_TYPE, str),
	(UNIT_MASTER_CARE_TYPEs, str),
	(UNIT_MASTER_CODEs, str),
	(UNITs, str),
	(VISID, str),
	(Vital_obs_type_count, str),
	(Vital_startTime, str),
	(Vital_stats, str),
	(Vital_stopTime, str),
	(WEIGHT_LBS, ta.float32),
	(ZIP, str),
    (uphs_id, str),
	(data_ts, str),
	(meds_data_raw, str),
	(orders_data_raw, str),
	# label columns
	(READMIT_30, str),
	(READMIT_90, str)
]


# the schema as dictionary that takes field name to its datatype
full_schema_dictionary = dict(full_schema)

# list of all fields used by the cardiac readmittance dataset
fields = full_schema_dictionary.keys()


"""
check that a given field name is a valid UPHS field name
"""

def check_field(f):
    if not f in fields:
        print "Bad field name : " + f + "\n"
        return False
    else:
        return True

"""
check that all field names in a collection are valid UPHS field names
"""
def check_fields(in_fields):
    return all(check_field(f) for f in in_fields)


"""
return the schema for a collection of UPHS cardiac field names

in_fields:  a collection of UPHS cardiac field names

return value: collection of (field_name, trustedaanalytics datatype) pairs (ie. the schema for these columns)
"""
def get_schema(in_fields):
    if (check_fields(in_fields)):
        return map(lambda field: (field, full_schema_dictionary[field]), in_fields)
    else:
        print "Bad field name, no schema produced."
        return []

