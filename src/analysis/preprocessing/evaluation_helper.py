import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix


class PipelineEvaluations:
    def __init__(self):
        pass

    @staticmethod
    def evaluate_gesture_classificaiton(y_test, y_pred):
        # Evaluate the model
        cls_rep = classification_report(y_test, y_pred)
        acc = accuracy_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)
        return acc, cls_rep, conf_matrix

    @staticmethod
    def evaluate_mpjpe(y_test, y_pred, pca=False):
        # Calculate the mpjpe
        error = (y_pred - y_test).reshape((-1, 21, 3)) * 1000
        error = np.linalg.norm(error, axis=2)
        # print(error)
        error_per_joint = np.mean(error, axis=0)
        std_per_joint = np.std(error, axis=0)
        # print(error_per_joint)
        error_total = np.mean(np.abs(error))
        std_total = np.std(error)
        # print(error_total, std_total)

        # Create an array with the indices
        # x_pos = np.arange(len(error_per_joint))
        hand_landmarks = [
            'Wrist',
            'Thumb_CMC', 'Thumb_MCP', 'Thumb_IP', 'Thumb_Tip',
            'Index_Finger_MCP', 'Index_Finger_PIP', 'Index_Finger_DIP', 'Index_Finger_Tip',
            'Middle_Finger_MCP', 'Middle_Finger_PIP', 'Middle_Finger_DIP', 'Middle_Finger_Tip',
            'Ring_Finger_MCP', 'Ring_Finger_PIP', 'Ring_Finger_DIP', 'Ring_Finger_Tip',
            'Pinky_MCP', 'Pinky_PIP', 'Pinky_DIP', 'Pinky_Tip'
        ]

        # Make the bar chart
        plt.bar(hand_landmarks, error_per_joint, yerr=std_per_joint, align='center', alpha=0.7, capsize=10)
        plt.xticks(hand_landmarks)
        plt.xticks(rotation=45, ha='right')


        plt.ylabel('Mean per joint position error (mm)')
        plt.title('Bar plot with error bars')

        # plt.show()
        return error_per_joint, std_per_joint, error_total, std_total, y_pred
