from pathlib import Path
import sys
from datetime import datetime
import logging

import numpy as np

path_to_root = Path('../../../') # path to top level PulsePose
path_to_experiment_results = path_to_root / 'src' / 'analysis' / 'evaluation' / 'experiment_results'
sys.path.append(str(path_to_root))

from src.analysis.preprocessing.data_loader import DataLoader
from src.analysis.evaluation.experiment import Experiment
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt


def log_print(*args, **kwargs):
    message = ' '.join(str(arg) for arg in args)
    logging.info(message)  # Log to the experiment-specific logger
    print(*args, **kwargs)  # Print to console


class ETRExperimentRunner:
    def __init__(self, experiment_params_list, experiment_author='anonymous', path_to_data=path_to_root / 'src' / 'data' / 'processed_data'):
        self.experiment_params_list = experiment_params_list
        self.author = experiment_author
        self.path_to_data = path_to_data

    def run(self):
        # Get the current date and time
        now = datetime.now()
        # Convert the date and time to a string in the format YYYYMMDD_HHMMSS
        save_time = now.strftime("%Y%m%d_%H%M%S")

        output_folder = path_to_experiment_results / str(self.author + "_" + save_time)
        output_folder.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(level=logging.DEBUG, 
                    filename=str(output_folder / str(self.author + '_experiment_log.log')), 
                    filemode='w', 
                    format='%(name)s - %(levelname)s - %(message)s')
        plt.set_loglevel("info") # suppresses matplotlib debug messages


        for i in range(len(self.experiment_params_list)):
            experiment = self.experiment_params_list[i]
            self.participant_list = experiment['participants']

            self.participant_dls = []
            for user in self.participant_list:
                session_dls = []
                for session in user:
                    recording_dls = []
                    for recording in session:
                        recording_dls.append(DataLoader(recording, self.path_to_data))
                    session_dls.append(recording_dls)
                self.participant_dls.append(session_dls)

            output = ''
            for evaluation_type, rounds in experiment['evaluations'].items():
                etr_exp = Experiment(self.participant_dls, experiment['experiment_params'], evaluation_type, rounds, log_print, output_folder)
                if experiment['experiment_params']['evaluator_type'] == 'classifier':
                    acc_mean, acc_std, acc_list, cls_rep_list, conf_matrix_list, save_location = etr_exp.run_experiment()
                    combined_conf_matrix = np.sum(np.stack(conf_matrix_list), axis=0)
                    normalized_conf_matrix = np.transpose(np.transpose(combined_conf_matrix) / np.sum(combined_conf_matrix, axis=1)) * 100.0

                    labels = np.array([
                        "fist", 
                        "spiderman", 
                        "OK", 
                        "claw", 
                        "stretch", 
                        "point", 
                        "pinch", 
                        "close", 
                        "three point", 
                        "gun", 
                        "six", 
                        "thumbs up",
                        "",
                        "open",
                        "down",
                        "up",
                        "left",
                        "right",
                    ])
                    drop_labels = experiment['experiment_params']['y_cols']['gesture_label']['exclude_values_no_drop'] + [12]
                    labels = np.delete(labels, drop_labels)
                    disp = ConfusionMatrixDisplay(confusion_matrix=normalized_conf_matrix, display_labels=labels)
                    fig, ax = plt.subplots(figsize=(10, 10))  # Adjust the figure size as needed
                    disp.plot(ax=ax)
                    # disp.plot()
                    plt.xticks(rotation=45)  # Rotate labels by 45 degrees, or any angle you prefer

                    plt.tight_layout()
                    plt.savefig(str(output_folder / (str(i) + '_' + str(evaluation_type) + '.png')))
                    plt.show()
                    output = '\n'.join([
                        f'Experiment Number: {i}',
                        f'Experiment parameters: {str(experiment)}',
                        f'Evaluation type: {str(evaluation_type)}',
                        f'Result: {str(acc_mean)}, {str(acc_std)}',
                        f'Accuracy List: {str(acc_list)}',
                        f'Combined Confusion Matrix: {str(combined_conf_matrix)}',
                        f'Normalized Confusion Matrix: {str(normalized_conf_matrix)}',
                        f'Confusion Matrices: {str(conf_matrix_list)}',
                        f'Classification Report List: {str(cls_rep_list)}',
                        f'Model Locations: {str(save_location)}',
                    ])
                else:
                    error, std, error_list_by_joint, std_list_by_joint, error_list_by_participant, std_list_by_participant, save_location = etr_exp.run_experiment()
                    output = '\n'.join([
                        f'Experiment Number: {i}',
                        f'Experiment parameters: {str(experiment)}',
                        f'Evaluation type: {str(evaluation_type)}',
                        f'Result: {str(error)}, {str(std)}',
                        f'Error List by Joint: {str(error_list_by_joint)}',
                        f'Std List by Joint: {str(std_list_by_joint)}',
                        f'Error List by Participant {str(error_list_by_participant)}',
                        f'Std List by by Participant {str(std_list_by_participant)}',
                        f'Model Locations: {str(save_location)}',
                    ])

                # save stats
                log_print(output)

            # text_file = open(path_to_experiment_results / (self.author + '_' + str(save_time) + '_' + str(i) + '.txt'), "w")
            # text_file.write(output)
            # text_file.close()


