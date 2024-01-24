from pathlib import Path
import sys

path_to_root = Path('../../../') # path to top level PulsePose
path_to_experiment_results = path_to_root / 'src' / 'analysis' / 'evaluation' / 'experiment_results'
sys.path.append(str(path_to_root))

from src.analysis.evaluation.experiments_runner import ETRExperimentRunner

from src.analysis.models.ETR import ETR

from src.analysis.preprocessing.evaluation_helper import PipelineEvaluations


experiment_params_list = [
    # Experiment 0
    {            
        'experiment_params': {
            'x_scale': False,
            'y_scale': False,
            'save_model': False,
            'save_y_pred': False,
            'x_cols': {
                'eit_data': {
                    'demean': False,
                    'individual_scale': False,
                    # 'rolling_demean_no_drop': 400
                    'rolling_demean_no_drop': {
                        'RR-U1-1': 400, 'RR-U1-2': 400, 'RR-U1-3': 400, 'RR-U1-4': 400, 
                        'RR-U2-1': 400, 'RR-U2-2': 400, 'RR-U2-3': 400, 'RR-U2-4': 400, 
                        'RR-U3-1': 400, 'RR-U3-2': 400, 'RR-U3-3': 400, 'RR-U3-4': 400, 
                    }
                },
            },
            'y_cols': {
                'mphands_scaled': {

                },
            },

            'model': ETR,
            'modelname': ETR.MODELNAME,
            'model_params': {
            },

            'evaluator': PipelineEvaluations.evaluate_mpjpe,
            'evaluator_type': 'mpjpe',
            'window': 1,
            'window_stride': 1,
            'data_shape': '1d',
            'gpu': '/GPU:2',
        },

        'participants': [ # inner most defines within session, then same user
            [['RR-U1-1'], ['RR-U1-2']],
            [['RR-U1-1'], ['RR-U1-3']],
            [['RR-U1-1'], ['RR-U1-4']],

            [['RR-U2-1'], ['RR-U2-2']],
            [['RR-U2-1'], ['RR-U2-3']],
            [['RR-U2-1'], ['RR-U2-4']],

            [['RR-U3-1'], ['RR-U3-2']],
            [['RR-U3-1'], ['RR-U3-3']],
            [['RR-U3-1'], ['RR-U3-4']],

        ],
        'evaluations': {
            'crosssession': 'all',
        },
    },
]


testrunner = ETRExperimentRunner(experiment_params_list, 'experiment_mpjpe_longitudinal', path_to_data=path_to_root / 'src' / 'data' / 'processed_longitudinal_data')
testrunner.run()
