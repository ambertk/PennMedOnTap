__author__ = 'nlsegerl'

"""
Filters used to validate data in the UPHS cardiac prediction analysis.
"""
from uphs_fields import *


"""
PATIENT ID and VISIT ID

These cannot be none and they have to have length 20.
(A few bad records with PATID/VISID nonstandard length IDs exist and I just throw them out.)
"""

def patid_filter(row):
    return row[PATID] != None and row[PATID] != 'None' and len(row[PATID]) == 20


def visid_filter(row):
    return row[VISID] != None and row[VISID] != 'None' and len(row[VISID]) == 20


"""
date filter

cannot be None
if a record doesn't have a date, it is useless to us and gets thrown out
"""

def adm_date_filter(row):
    return row[ADM_DATE] != None

"""
emergency_admit_filter

Keep only emergency visits
"""

def emergency_admit_filter(row):
    return row[ADMIT_TYPE] != None and row[ADMIT_TYPE].lower() == 'emergency'
