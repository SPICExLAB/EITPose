from pathlib import Path
import os

import numpy as np
import pandas as pd
from sklearn import preprocessing
from scipy.spatial.transform import Rotation as R


path_to_root = Path('../../../') # path to top level PulsePose
path_to_processed_data = path_to_root / 'src' / 'data' / 'processed_data'

# import sys
# sys.path.append(str(path_to_root))


class DataLoader:
    def __init__(self, participant, path=path_to_processed_data):
        self.participant = participant
        self.dataframe = pd.read_pickle(str(path / (participant + '_processed.pkl')))
        # f = open(str(path / (participant + '_processed_stats.txt')), "r")
        # self.stats = f.read()
        # print("Loaded Participant: ")
        # print(self.stats)
    
        self.individual_scaler = preprocessing.MinMaxScaler()

    def get_dataframe(self):
        return self.dataframe
    
    def individual_scale(self, data):
        return self.individual_scaler.fit_transform(data)

    def demean(self, data):
        return data - np.mean(data, axis=0)

    def rolling_demean(self, data, window_size=20):
        rolling_mean = pd.DataFrame(data).rolling(window_size).mean().to_numpy()
        return data - rolling_mean

    def rolling_demean_no_drop(self, data, window_size=20):
        early_rolling_mean = []
        for i in range(window_size):
            early_rolling_mean.append(np.mean(data[:i+1], axis=0))
        rolling_mean = pd.DataFrame(data).rolling(window_size).mean().to_numpy()
        rolling_mean[:window_size] = np.array(early_rolling_mean)
        return data - rolling_mean

    def rolling_demean_no_drop_future(self, data, window_size=20):
        early_rolling_mean = []
        for i in range(window_size):
            early_rolling_mean.append(np.mean(data[:window_size], axis=0))
        rolling_mean = pd.DataFrame(data).rolling(window_size).mean().to_numpy()
        rolling_mean[:window_size] = np.array(early_rolling_mean)
        return data - rolling_mean

    def diff(self, data):
        diff = pd.DataFrame(data).diff().to_numpy()
        return diff

    def standardize_wrist_rotation_imu(self, data): # for IMU Data
        # init_mat = R.from_matrix(data[0, 9:].reshape((3, 3)))
        imu_output = data[:, 9:].reshape((-1, 3, 3))
        rot_vect_imu_output = []
        for i in range(len(imu_output)):
            init_mat = imu_output[0]
            # R_base_T = R[0].T
            R_normalized = np.dot(init_mat.T, imu_output[i])
            rot_vect_imu_output.append(np.array(R.from_matrix(R_normalized).as_rotvec()))
        return np.array(rot_vect_imu_output)

    def standardize_wrist_rotation_mediapipe(self, data):
        def _hand_normalize(x):
            res = x / np.linalg.norm(x)
            return res
        def get_palm_normal(hand_data): # for 
            hand_data = hand_data.reshape((21, 3))
            v05 = hand_data[5]-hand_data[0]
            v017 = hand_data[17]-hand_data[0]
            normal = _hand_normalize(np.cross(v017,v05))
            y_axis = _hand_normalize(normal)
            return y_axis



        # NOTE: do i need to normalize? see align_palm_normals below
        palm_normals = np.apply_along_axis(get_palm_normal, 1, data)
        return palm_normals

    def exclude_values_no_drop(self, data, exclude_list):
        for val in exclude_list:
            data[data == val] = np.nan
        return data

    def convert_values(self, data, conversion_dict):
        for k, v in conversion_dict.items():
            data[data == k] = v
        return data

    def align_palm_normals(self, data):
        def align_to_reference(normal, reference=[0, 0, 1]):
            """Align the given normal to the reference direction."""
            # Calculate the rotation axis (which is perpendicular to the plane formed by normal and reference)
            rot_axis = np.cross(normal, reference)
            rot_axis /= np.linalg.norm(rot_axis)  # normalize the axis

            # Calculate the angle between normal and reference
            cos_angle = np.dot(normal, reference)
            angle = np.arccos(cos_angle)

            # Create a rotation matrix using the axis and the angle
            rotation = R.from_rotvec(rot_axis * angle)
            
            return rotation
        rotation_to_starter = align_to_reference(data[0])

        aligned_normals_list = []
        for palm_normal in data:
            aligned_normal = rotation_to_starter.apply(palm_normal)
            aligned_normals_list.append(aligned_normal)
        return np.array(aligned_normals_list)

    def scale(self, data, scale_factor):
        return scale_factor*data
    

    def get_subset_data_concatenated(self, cols):
        total_dat = None
        for col_name, data_alterations in cols.items():
            if col_name != 'sample_weights':
                numpy_arr_temp = np.stack(self.dataframe[col_name])
            else:
                numpy_arr_temp = np.ones(len(self.dataframe))

            for alteration in data_alterations.keys():
                if alteration == 'individual_scale' and data_alterations[alteration]:
                    numpy_arr_temp = self.individual_scale(numpy_arr_temp)
                elif alteration == 'demean' and data_alterations[alteration]:
                    numpy_arr_temp = self.demean(numpy_arr_temp)
                elif alteration == 'rolling_demean' and data_alterations[alteration] != 0:
                    numpy_arr_temp = self.rolling_demean(numpy_arr_temp, data_alterations[alteration])
                elif alteration == 'scale' and type(data_alterations[alteration]) is dict and data_alterations[alteration][self.participant] != 0:
                    numpy_arr_temp = self.scale(numpy_arr_temp, data_alterations[alteration][self.participant])
                elif alteration == 'scale' and data_alterations[alteration] != 0:
                    numpy_arr_temp = self.scale(numpy_arr_temp, data_alterations[alteration])
                elif alteration == 'rolling_demean_no_drop' and type(data_alterations[alteration]) is dict and data_alterations[alteration][self.participant] != 0:
                    numpy_arr_temp = self.rolling_demean_no_drop(numpy_arr_temp, data_alterations[alteration][self.participant])
                elif alteration == 'rolling_demean_no_drop' and data_alterations[alteration] != 0:
                    numpy_arr_temp = self.rolling_demean_no_drop(numpy_arr_temp, data_alterations[alteration])
                elif alteration == 'rolling_demean_no_drop_future' and type(data_alterations[alteration]) is dict and data_alterations[alteration][self.participant] != 0:
                    numpy_arr_temp = self.rolling_demean_no_drop_future(numpy_arr_temp, data_alterations[alteration][self.participant])
                elif alteration == 'rolling_demean_no_drop_future' and data_alterations[alteration] != 0:
                    numpy_arr_temp = self.rolling_demean_no_drop_future(numpy_arr_temp, data_alterations[alteration])
                elif alteration == 'diff' and data_alterations[alteration]:
                    numpy_arr_temp = self.diff(numpy_arr_temp)
                elif alteration == 'standardize_wrist_rotation_imu' and data_alterations[alteration]:
                    numpy_arr_temp = self.standardize_wrist_rotation_imu(numpy_arr_temp)
                elif alteration == 'standardize_wrist_rotation_mediapipe' and data_alterations[alteration]:
                    numpy_arr_temp = self.standardize_wrist_rotation_mediapipe(numpy_arr_temp)
                elif alteration == 'align_palm_normals' and data_alterations[alteration]:
                    numpy_arr_temp = self.align_palm_normals(numpy_arr_temp)
                elif alteration == 'exclude_values_no_drop' and (type(data_alterations[alteration]) is list or type(data_alterations[alteration]) is tuple):
                    numpy_arr_temp = self.exclude_values_no_drop(numpy_arr_temp, data_alterations[alteration])
                elif alteration == 'convert_values' and type(data_alterations[alteration]) is dict:
                    numpy_arr_temp = self.convert_values(numpy_arr_temp, data_alterations[alteration])

            if total_dat is not None:
                total_dat = np.hstack((total_dat, numpy_arr_temp))
            else:
                total_dat = numpy_arr_temp
        return total_dat
