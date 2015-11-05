__author__ = 'nlsegerl'

# UDF paths

uphs_fields = 'uphs_fields.py'
uphs_schema = 'uphs_schema.py'
uphs_loader = 'uphs_loader.py'
filters = 'filters.py'
clean_drugs = 'clean_drugs.py'
history_utilities = 'history_utilities.py'
ground_truth_utilities = 'ground_truth_utils.py'
derived_features = 'derived_features.py'
historical_features_schema = 'historical_features_schema.py'


"""
Utilities for managing UDF file installations for trustedanalytics.

WARNING

Current trustedanalytics behavior is for subsequent calls to udf.install() to wipe out the previous install list

eg.
In [7]: ta.udf.list()
Out[7]:
['clean_drugs.py',
 'ground_truth_utils.py',
 'filters.py',
 'derived_features.py',
 <module 'history_features' from '/home/hadoop/UPHS_Intel/full_readmit_on_atk/history_features.py'>,
 'historical_features_schema.py',
 'uphs_fields.py',
 'uphs_loader.py',
 'uphs_schema.py',
 'history_utilities.py']

In [8]: ta.udf.install('clean_drugs.py')

In [9]: ta.udf.list()
Out[9]: 'clean_drugs.py'

So you have to be careful about call udf.install()... you might lose things that you thought were previously installed.
"""


"""
Install all of the UDF files. Overwrites the UDF installation list.
"""
def install_all_udf_files(ta):
    return ta.udf.install([uphs_fields, filters, clean_drugs, history_utilities, ground_truth_utilities, historical_features_schema])


"""
Non-destructively ADD files to the current UDF installation list.
"""
def add_udf_files(ta, module_list):

    install_set = set(ta.udf.list())

    for m in module_list:
        install_set.add(m)

    ta.udf.install(list(install_set))

    return