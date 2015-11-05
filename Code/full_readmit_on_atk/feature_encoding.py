__author__ = 'nlsegerl'

"""
Convert string feature into a numerical (integer) feature for ingestion by random forest.

modifies the given frame

Assumes that the feature take relatively few distinct and that it will not be too expensive to make the column
distinct and pull distinct values to the local Python session.

This is a reasonable assumption as the procedure is meant for string categorial variables.
"""
def numericalize_feature(ta, in_frame, in_column_name, new_column_name):

    print "****** NUMERICALIZING FEATURE:  " + in_column_name
    # we need a copy of the frame with only the target column
    print "****** creating temporary copy of frame "  + in_frame.name + " for determination of distinct values in column " + in_column_name
    working_frame = in_frame.copy()
    cols_to_drop = [col for (col, type) in in_frame.schema]
    cols_to_drop.remove(in_column_name)
    working_frame.drop_columns(cols_to_drop)

    print "****** determining unique values in column " + in_column_name
    working_frame.drop_duplicates()

    frame = working_frame.download()

    # this produces a dictionary for count position (int) to field name
    d = frame.to_dict()[in_column_name]

    rev_dict = dict((v, k) for k, v in d.iteritems())

    def numericalize_udf(in_val):
        return rev_dict[in_val]

    print "****** assigning numericalized values of column " + in_column_name + " to new column " + new_column_name

    in_frame.add_columns(lambda row: numericalize_udf(row[in_column_name]), (new_column_name, ta.int32))

    #clean up that extra frame!
    ta.drop_frames(working_frame)

    return in_frame

"""
numericalize each feature in a list

Returns a modified copy of the input frame in which
column names of new frame match those of incoming frame, but the schame has been changed so that
the modified columns are of integer type.
"""

def numericalize_frame(ta, in_frame, frame_name, target_cols, overwrite = True):
    print "*** Numericalizing string features of frame " + in_frame.name
    print "*** Frame with numerical features: " + frame_name

    if (frame_name in ta.get_frame_names()):
        if (not overwrite):
            return ta.get_frame(frame_name)
        else:
            ta.drop_frames([frame_name])

    numericalized_frame = in_frame.copy(name = frame_name)


    for col in target_cols:
        numericalize_feature(ta, numericalized_frame, col, col + "_INT")

    numericalized_frame.drop_columns(target_cols)
    numericalized_frame.rename_columns( { col + "_INT": col for col in target_cols })
    return numericalized_frame
