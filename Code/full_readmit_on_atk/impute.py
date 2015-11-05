

"""
Perform imputation by a constant on a set of columns.
Input takes a dictionary matching column names to imputation values, which will replace any Nones.

This operation is in-place and modifies the incoming dataframe.
"""

def impute_with_constants(frame, column_default_value_dict):
    columns_to_impute  = column_default_value_dict.keys()

    old_schema_dict = dict(frame.schema)

    new_columns_schema = []
    rename_dict = {}

    for c in columns_to_impute:
        new_columns_schema.append((c+"_new", old_schema_dict[c]))
        rename_dict[ c + "_new"] = c

    # GRUMBLE:  it's so annoyting that to do imputation we have to do an add columns/rename columns/drop columns...
    # that's THREE trustedanalytics calls with all that overhead

    frame.add_columns(lambda row: map (lambda col: column_default_value_dict[col] if row[col] == None else row[col], columns_to_impute),
                      new_columns_schema)
    frame.drop_columns(columns_to_impute)
    frame.rename_columns(rename_dict)
    return frame