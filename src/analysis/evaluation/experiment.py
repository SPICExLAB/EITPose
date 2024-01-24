from pathlib import Path
import sys
import pickle
from datetime import datetime

import numpy as np
from sklearn import preprocessing

path_to_root = Path('../../../') # path to top level PulsePose
path_to_models = path_to_root / 'src' / 'analysis' / 'models'
path_to_y_pred = path_to_root / 'src' / 'analysis' / 'y_pred'
sys.path.append(str(path_to_root))

from src.analysis.preprocessing.data_splitter_v2 import DataSplitter
from src.analysis.preprocessing.helper_functions import scale_window_reshape



class Experiment:
    def __init__(self, participant_dls, experiment_params, evaluation, rounds='all', print_fcn=None):
        self.participant_dls = participant_dls
        self.evaluation = evaluation
        self.x_cols = experiment_params['x_cols']
        self.y_cols = experiment_params['y_cols']
        self.experiment_params = experiment_params
        self.model = experiment_params['model']
        self.evaluator_type = experiment_params['evaluator_type']
        self.evaluator = experiment_params['evaluator']
        self.window = experiment_params['window']
        self.window_stride = experiment_params['window_stride']
        self.data_shape = experiment_params['data_shape']
        self.num_rounds = rounds
        if 'gpu' in experiment_params.keys():
            self.gpu = experiment_params['gpu']
        else:
            self.gpu = '/GPU:0'

        if print_fcn:
            self.print_fcn = print_fcn
        else:
            self.print_fcn = print

        self.data_splitter = DataSplitter(self.participant_dls)
        if self.evaluation == 'withinsession':
            self.splitter = self.data_splitter.create_within_session_split_generator
        elif self.evaluation == 'crosssession':
            self.splitter = self.data_splitter.create_cross_session_split_generator
        elif self.evaluation == 'crosssession_full':
            self.splitter = self.data_splitter.create_cross_session_with_all_users_split_generator
        elif self.evaluation == 'crossuser':
            self.splitter = self.data_splitter.create_cross_user_split_generator
        elif self.evaluation == 'withinsession_kfold':
            self.splitter = self.data_splitter.create_within_session_k_fold

    def run_experiment(self):
        self.print_fcn("Running Experiment: ")

        error_per_joint_list = []
        std_per_joint_list = []
        acc_list = []
        cls_rep_list = []
        conf_matrix_list = []

        model_list = []
        X_scaler_list = []
        y_scaler_list = []
        evaluation = self.evaluator_type
        modelname = self.model.MODELNAME

        window_size = self.window
        stride = self.window_stride
        shape = self.data_shape
        round_counter = 0

        for X_train, y_train, X_test, y_test, train_participants, test_participants in self.splitter(self.x_cols, self.y_cols):
            # # NOTE: ONLY USE THIS IF TRYING TO SKIP CERTAIN EXPERIMENTS
            # if round_counter < 16: # skip up to and including W
            #     round_counter += 1
            #     continue

            # print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)
            round_counter += 1

            # Some data alterations creates nan's remove rows
            nan_rows_train = np.all(np.isnan(X_train), axis=1)
            nan_rows_test = np.all(np.isnan(X_test), axis=1)
            if evaluation == 'classifier':
                nan_rows_train_y = np.isnan(y_train)
                nan_rows_test_y = np.isnan(y_test)
                X_train = X_train[[(~nan_rows_train)[i] and (~nan_rows_train_y)[i] for i in range(len(X_train))]]
                X_test = X_test[[(~nan_rows_test)[i] and (~nan_rows_test_y)[i] for i in range(len(X_test))]]
                y_train = y_train[[(~nan_rows_train)[i] and (~nan_rows_train_y)[i] for i in range(len(y_train))]]
                y_test = y_test[[(~nan_rows_test)[i] and (~nan_rows_test_y)[i] for i in range(len(y_test))]]
                y_train = y_train.astype(int)
                y_test = y_test.astype(int)
            else:
                X_train = X_train[~nan_rows_train]
                X_test = X_test[~nan_rows_test]
                y_train = y_train[~nan_rows_train]
                y_test = y_test[~nan_rows_test]
 
            # print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)
            
            if self.experiment_params['x_scale']:
                X_scaler = preprocessing.MinMaxScaler()
                X_train, y_train, X_test, y_test, X_scaler = scale_window_reshape(X_train, y_train, X_test, y_test, X_scaler, window_size, stride, shape)
            else:
                X_train, y_train, X_test, y_test, X_scaler = scale_window_reshape(X_train, y_train, X_test, y_test, None, window_size, stride, shape)

            if self.experiment_params['y_scale']:
                y_scaler = preprocessing.MinMaxScaler()
                y_train = y_scaler.fit_transform(y_train)
                y_test = y_scaler.transform(y_test)

            if modelname != 'extratreesregressor' and modelname != 'extratreesclassifier':
                X_val = X_test[0:int(0.5*len(X_test))]
                X_test = X_test[int(0.5*len(X_test)):]
                y_val = y_test[0:int(0.5*len(y_test))]
                y_test = y_test[int(0.5*len(y_test)):]
                self.print_fcn("X_train shape: ", X_train.shape, "y_train shape: ", y_train.shape, "X_test shape: ", X_test.shape, "y_test shape: ", y_test.shape, "X_val shape: ", X_val.shape, "y_val shape: ", y_val.shape)
            else:
                X_val = None
                y_val = None
                self.print_fcn("X_train shape: ", X_train.shape, "y_train shape: ", y_train.shape, "X_test shape: ", X_test.shape, "y_test shape: ", y_test.shape)
            
            if self.evaluation == 'withinsession_kfold':
                self.print_fcn("Evaluating: ", ''.join(train_participants), "K: ", ''.join(test_participants))
            else:
                self.print_fcn("Train on: ", ''.join(train_participants), "Test on: ", ''.join(test_participants))

            if evaluation != 'classifier':

                if modelname != 'extratreesregressor':
                    model = self.model()
                    model.set_params(self.experiment_params['model_params'])
                    model = model.train(X_train, y_train, X_val, y_val)
                    model_list.append([''.join(train_participants), ''.join(test_participants), model])
                    
                    if self.experiment_params['x_scale']:
                        X_scaler_list.append([''.join(train_participants), ''.join(test_participants), X_scaler])
                    
                    y_pred = model.predict(X_test)

                    if self.experiment_params['y_scale']:
                        y_pred = y_scaler.inverse_transform(y_pred)
                        y_test = y_scaler.inverse_transform(y_test)
                        y_scaler_list.append([''.join(train_participants), ''.join(test_participants), y_scaler])

                    if self.evaluator_type == 'wrist_angle':
                        error_per_joint, std_per_joint, y_pred = self.evaluator(y_test, y_pred)
                        self.print_fcn(error_per_joint)
                    else:
                        error_per_joint, std_per_joint, error_total, std_total, y_pred = self.evaluator(y_test, y_pred)
                        self.print_fcn(error_per_joint)
                        self.print_fcn(error_total, std_total)

                    error_per_joint_list.append(error_per_joint)
                    std_per_joint_list.append(std_per_joint)

                        
                else:
                    model = self.model()
                    model.set_params(self.experiment_params['model_params'])
                    model = model.train(X_train, y_train, X_val, y_val)
                    model_list.append([''.join(train_participants), ''.join(test_participants), model])
                    
                    if self.experiment_params['x_scale']:
                        X_scaler_list.append([''.join(train_participants), ''.join(test_participants), X_scaler])
                    
                    y_pred = model.predict(X_test)

                    if self.experiment_params['y_scale']:
                        y_pred = y_scaler.inverse_transform(y_pred)
                        y_test = y_scaler.inverse_transform(y_test)
                        y_scaler_list.append([''.join(train_participants), ''.join(test_participants), y_scaler])

                    if self.evaluator_type == 'wrist_angle':
                        error_per_joint, std_per_joint, y_pred = self.evaluator(y_test, y_pred)
                        self.print_fcn(error_per_joint)
                    else:
                        error_per_joint, std_per_joint, error_total, std_total, y_pred = self.evaluator(y_test, y_pred)
                        self.print_fcn(error_per_joint)
                        self.print_fcn(error_total, std_total)

                    if 'save_y_pred' in self.experiment_params.keys() and self.experiment_params['save_y_pred']:
                        # Get the current date and time
                        now = datetime.now()
                        # Convert the date and time to a string in the format YYYYMMDD_HHMMSS
                        save_time = now.strftime("%Y%m%d_%H%M%S")
                        filename = path_to_y_pred / modelname / evaluation / self.evaluation
                        Path.mkdir(filename, parents=True, exist_ok=True)
                        np.save(str(filename / str(''.join(train_participants) + '_'  + ''.join(test_participants) + '_' + save_time)), y_pred)

                    error_per_joint_list.append(error_per_joint)
                    std_per_joint_list.append(std_per_joint)

                    self.print_fcn(error_per_joint)
                    self.print_fcn(error_total, std_total)

                if self.num_rounds != 'all' and (round_counter >= self.num_rounds):
                    break
        
            else:
                # classification evaluation
                model = self.model()
                model.set_params(self.experiment_params['model_params'])
                model = model.train(X_train, y_train, X_val, y_val)
                model_list.append([''.join(train_participants), ''.join(test_participants), model])
                
                if self.experiment_params['x_scale']:
                    X_scaler_list.append([''.join(train_participants), ''.join(test_participants), X_scaler])
                
                y_pred = model.predict(X_test)

                # if self.experiment_params['y_scale']:
                #     y_pred = y_scaler.inverse_transform(y_pred)
                #     y_test = y_scaler.inverse_transform(y_test)
                #     y_scaler_list.append([''.join(train_participants), ''.join(test_participants), y_scaler])

                acc, cls_rep, conf_matrix = self.evaluator(y_test, y_pred)
                self.print_fcn("Accuracy: ", acc)
                self.print_fcn(cls_rep)
                self.print_fcn(conf_matrix)
                acc_list.append(acc)
                cls_rep_list.append(cls_rep)
                conf_matrix_list.append(conf_matrix)

                self.print_fcn(acc)
                self.print_fcn(cls_rep)
                self.print_fcn(conf_matrix)

        if evaluation != 'classifier':
            error_per_joint_list = np.array(error_per_joint_list)
            std_per_joint_list = np.array(std_per_joint_list)
            if self.evaluator_type != 'wrist_angle':
                self.print_fcn("Mean Error Per Joint: ", np.mean(error_per_joint_list, axis=0))
            self.print_fcn("Mean Error: ", np.mean(error_per_joint_list), "Std Error: ", np.mean(std_per_joint_list))

        filename = 'None'
        if self.experiment_params['save_model']:
            # Get the current date and time
            now = datetime.now()
            # Convert the date and time to a string in the format YYYYMMDD_HHMMSS
            save_time = now.strftime("%Y%m%d_%H%M%S")
            filename = path_to_models / modelname / evaluation / self.evaluation / save_time
            Path.mkdir(filename, parents=True, exist_ok=True)

            for trainname, testname, model in model_list:
                model.save_model(filename / (trainname + "_" + testname + "_" + save_time))
                self.print_fcn("Saved Model: ", filename / (modelname + '_' + trainname + "_" + testname + "_" + save_time))

            for trainname, testname, X_scaler in X_scaler_list:
                x_scale_dir = str(filename / ('xscaler_' + trainname + "_" + testname + "_" + save_time + '.pkl'))
                pickle.dump(X_scaler ,open(x_scale_dir,'wb'))
                self.print_fcn("Saved X_scaler: ", x_scale_dir)

            for trainname, testname, y_scaler in y_scaler_list:
                y_scale_dir = str(filename / ('yscaler_' + trainname + "_" + testname + "_" + save_time + '.pkl'))
                pickle.dump(X_scaler ,open(y_scale_dir,'wb'))
                self.print_fcn("Saved y_scaler: ", y_scale_dir)
            
        
        if evaluation == 'classifier':
            return np.mean(acc_list), np.std(acc_list), acc_list, cls_rep_list, conf_matrix_list, filename
        # return np.mean(error_per_joint_list), np.std(np.mean(error_per_joint_list, axis=0)), np.mean(error_per_joint_list, axis=0), np.mean(std_per_joint_list, axis=0), np.mean(error_per_joint_list, axis=1), np.mean(std_per_joint_list, axis=1), filename
        return np.mean(error_per_joint_list), np.std(np.mean(error_per_joint_list, axis=0)), np.mean(error_per_joint_list, axis=0), np.std(error_per_joint_list, axis=0), np.mean(error_per_joint_list, axis=1), np.std(error_per_joint_list, axis=1), filename


        

        

        