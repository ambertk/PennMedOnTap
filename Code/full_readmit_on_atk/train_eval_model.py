__author__ = 'nlsegerl'


from uphs_fields import  *

def build_eval_model(ta, model_name, training_frame, test_frame, target_column, observation_columns, overwrite = True):

    if (model_name in ta.get_model_names()):
        if (not overwrite):
            return ta.get_model(model_name)
        else:
            ta.drop_models([model_name])


    rf_model = ta.RandomForestClassifierModel(model_name)

    rd_train_results = rf_model.train(training_frame, target_column, observation_columns, num_trees = 100,
                                           feature_subset_category = 'log2',
                                           max_depth = 15)


    print "Performance Metrics on Test Data"

    # test the model
    x = rf_model.test(test_frame, READMIT_30)
    print x