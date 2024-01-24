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
                        'U1-S1-T1': 400, 'U1-S1-T2': 400, 'U1-S2-T1': 400,
                        'U2-S1-T1': 400, 'U2-S1-T2': 400, 'U2-S2-T1': 400,
                        'U3-S1-T1': 400, 'U3-S1-T2': 400, 'U3-S2-T1': 400,
                        'U4-S1-T1': 400, 'U4-S1-T2': 400, 'U4-S2-T1': 400,
                        'U5-S1-T1': 400, 'U5-S1-T2': 400, 'U5-S2-T1': 400,
                        'U6-S1-T1': 400, 'U6-S1-T2': 400, 'U6-S2-T1': 400,
                        'U7-S1-T1': 400, 'U7-S1-T2': 400, 'U7-S2-T1': 400,
                        'U8-S1-T1': 400, 'U8-S1-T2': 400, 'U8-S2-T1': 400,
                        'U9-S1-T1': 400, 'U9-S1-T2': 400, 'U9-S2-T1': 400,
                        'U10-S1-T1': 400, 'U10-S1-T2': 400, 'U10-S2-T1': 400,
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
            [['U1-S1-T1', 'U1-S1-T2'], ['U1-S2-T1']], 
            [['U2-S1-T1', 'U2-S1-T2'], ['U2-S2-T1']], 
            [['U3-S1-T1', 'U3-S1-T2'], ['U3-S2-T1']], 
            [['U4-S1-T1', 'U4-S1-T2'], ['U4-S2-T1']], 
            [['U5-S1-T1', 'U5-S1-T2'], ['U5-S2-T1']], 
            [['U6-S1-T1', 'U6-S1-T2'], ['U6-S2-T1']], 
            [['U7-S1-T1', 'U7-S1-T2'], ['U7-S2-T1']], 
            [['U8-S1-T1', 'U8-S1-T2'], ['U8-S2-T1']], 
            [['U9-S1-T1', 'U9-S1-T2'], ['U9-S2-T1']], 
            [['U10-S1-T1', 'U10-S1-T2'], ['U10-S2-T1']], 

        ],
        'evaluations': {
            'crosssession': 'all',
        },
    },
]


testrunner = ETRExperimentRunner(experiment_params_list, 'experiment_mpjpe_cross_session', path_to_data=path_to_root / 'src' / 'data' / 'processed_pose_data')
testrunner.run()
