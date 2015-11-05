__author__ = 'nlsegerl'

"""
These are the column (feature) names (and their values, for string categoricals)
for the features that we compute during the analysis
as opposed from the ones that appear in the raw data from UPHS.
"""

CROSS_VALIDATION_CLASS  = 'CROSS_VALIDATION_CLASS'
TRAIN_LABEL = 'TRAIN'  # cross validation uses a simple train/test split,
TEST_LABEL = 'TEST'    # and these are the labels of the respective classes

EVENT_ID = 'EVENT_ID'  # concatentation of PATID and VISID to make up for lack of compound key functionality

UNCLEAN_COMBINED_MEDLIST = 'UNCLEAN_COMBINED_MEDLIST'  # raw drug list for a visit
COMBINED_MEDLIST = 'COMBINED_MEDLIST'  # cleaned drug list for a visit



INPAT_HISTORICAL_MEDLIST = 'INPAT_HISTORICAL_MEDLIST'   # prior 90 days combined clean drug lists