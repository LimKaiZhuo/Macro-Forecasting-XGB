from own_package.poos import poos_experiment, poos_analysis
from own_package.others import create_results_directory
from own_package.features_labels import read_excel_data, read_excel_dataloader, Fl_master, Fl_pca, Fl_ar, \
    Fl_cw, Fl_xgb, hparam_selection

import numpy as np
import pandas as pd
import pickle




def selector(case, **kwargs):
    if case == 1:
        # Run poos experiment
        var_name = kwargs['var_name']
        excel_dir = kwargs['excel_dir']
        results_dir = create_results_directory('./results/exptg/{}'.format(var_name))
        output = read_excel_dataloader(excel_dir=excel_dir)
        fl_master = Fl_master(x=output[0], features_names=output[1],
                              yo=output[2], labels_names=output[3],
                              y=output[4], y_names=output[5],
                              time_stamp=output[6])
        fl_xgb = Fl_xgb(val_split=None, x=None, yo=None, y=None,
                        time_stamp=None, time_idx=None,
                        features_names=fl_master.features_names, labels_names=fl_master.labels_names,
                        y_names=fl_master.y_names)

        first_est_date = '1970:1'

        model_mode = 'xgb_with_hparam'
        if model_mode == 'xgb' or model_mode == 'xgb_with_hparam':
            default_hparams = {'seed': 42,
                               'booster': 'gbtree',
                               'learning_rate': 0.1,
                               'objective': 'reg:squarederror',
                               'verbosity': 0,
                               'subsample': 1,
                               'num_boost_round': 600,
                               'early_stopping_rounds': 100,
                               'ehat_eval': None,
                               # 'eval_metric':['rmse'],
                               # DART params
                               'rate_drop': 0.2,
                               'skip_drop': 0.5,
                               # params that will vary
                               'm': 6,
                               'p': 12,
                               'max_depth': 1,
                               'colsample_bytree': 0.5,
                               }
            hparam_opt_params = {'hparam_mode': 'bo', 'n_calls': 200, 'n_random_starts': 150,
                                 'val_mode': 'rep_holdout',
                                 'n_blocks': 5, 'cut_point': 0.95,
                                 'variables': {'max_depth': {'type': 'Integer', 'lower': 1, 'upper': 6},
                                               'colsample_bytree': {'type': 'Real', 'lower': 0.5, 'upper': 1},
                                               'm': {'type': 'Integer', 'lower': 1, 'upper': 24},
                                               # 'p': {'type': 'Integer', 'lower': 1, 'upper': 48},
                                               'adap_gamma': {'type': 'Real', 'lower': -2, 'upper': 1.5}
                                               },
                                 }
        elif model_mode == 'rf':
            default_hparams = {'seed': 42,
                               'booster': 'gbtree',
                               'learning_rate': 1,
                               'objective': 'reg:squarederror',
                               'verbosity': 0,
                               'subsample': 1,
                               'num_boost_round': 1,
                               'early_stopping_rounds': None,
                               'ehat_eval': None,
                               # 'eval_metric':['rmse'],
                               # params that will vary
                               'm': 6,
                               'p': 12,
                               'max_depth': 1,
                               'colsample_bytree': 1,
                               }
            hparam_opt_params = {'hparam_mode': 'bo', 'n_calls': 200, 'n_random_starts': 150,
                                 'val_mode': 'rfcv',
                                 'n_blocks': 5, 'cut_point': 0.95,
                                 'variables': {'max_depth': {'type': 'Integer', 'lower': 1, 'upper': 6},
                                               'subsample': {'type': 'Real', 'lower': 0.5, 'upper': 1},
                                               'colsample_bytree': {'type': 'Real', 'lower': 0.5, 'upper': 1},
                                               'm': {'type': 'Integer', 'lower': 1, 'upper': 24},
                                               # 'p': {'type': 'Integer', 'lower': 1, 'upper': 48},
                                               'num_parallel_tree': {'type': 'Integer', 'lower': 1, 'upper': 1200}
                                               },
                                 }
        else:
            default_hparams=None
            hparam_opt_params = None

        est_dates = [f'{x}:12' for x in range(1969, 2020, 5)[:-1]]
        poos_experiment(fl_master=fl_master, fl=fl_xgb, est_dates=est_dates, z_type=1, h=1, h_idx=0,
                        m_max=12, p_max=24, model_mode=model_mode, save_dir=results_dir, first_est_date=first_est_date,
                        default_hparams=default_hparams, hparam_opt_params=hparam_opt_params,
                        set_hparam=kwargs['set_hparam']
                        )
        poos_experiment(fl_master=fl_master, fl=fl_xgb, est_dates=est_dates, z_type=1, h=3, h_idx=1,
                        m_max=12, p_max=24, model_mode=model_mode, save_dir=results_dir,first_est_date=first_est_date,
                        default_hparams=default_hparams, hparam_opt_params=hparam_opt_params,
                        set_hparam=kwargs['set_hparam']
                        )
        #poos_experiment(fl_master=fl_master, fl=fl_xgb, est_dates=est_dates, z_type=1, h=6, h_idx=2,
        #                m_max=12, p_max=24, model_mode=model_mode, save_dir=results_dir,first_est_date=first_est_date,
        #                default_hparams=default_hparams, hparam_opt_params=hparam_opt_params,
        #                set_hparam=kwargs['set_hparam']
        #                )
        poos_experiment(fl_master=fl_master, fl=fl_xgb, est_dates=est_dates, z_type=1, h=12, h_idx=3,
                        m_max=12, p_max=24, model_mode=model_mode, save_dir=results_dir,first_est_date=first_est_date,
                        default_hparams=default_hparams, hparam_opt_params=hparam_opt_params,
                        set_hparam=kwargs['set_hparam']
                        )
        poos_experiment(fl_master=fl_master, fl=fl_xgb, est_dates=est_dates, z_type=1, h=24, h_idx=4,
                        m_max=12, p_max=24, model_mode=model_mode, save_dir=results_dir,first_est_date=first_est_date,
                        default_hparams=default_hparams, hparam_opt_params=hparam_opt_params,
                        set_hparam=kwargs['set_hparam']
                        )

def prep_hparams(analysis_results_store):
    set_hparams = {}
    est_dates = [f'{x}:12' for x in range(1969, 2020, 5)[:-1]]
    for h in [1,3,6,12,24]:
        with open(analysis_results_store[h], 'rb') as handle:
            data_store = pickle.load(handle)
        hparam = {}
        for idx, est_date in enumerate(est_dates):
            hparam_dict = data_store['hparam_df'].iloc[idx,:].to_dict()
            rw_store = data_store['data_df']['rw_ntree'].loc[data_store['data_df']['hparam_block']==idx]
            hparam[est_date] = [{**hparam_dict, **{'num_boost_round':num+1}} for num in rw_store]
        set_hparams[h] = hparam
    return set_hparams


if __name__ == '__main__':
    set_hparam = {h: {'max_depth': 3, 'colsample_bytree': 0.75, 'm': 6, 'adap_gamma': 0, 'm iters': 100}
                  for h in [1,3,6,12,24]}
    set_hparam = prep_hparams({h: f'./results/poos/poos_CPIA1_xgba_rh_s42/poos_xgb_h{h}_analysis_results.pkl' for h in [1,3,6,12,24]})
    selector(case=1, excel_dir='./excel/dataset_0720/CPIA1s_data_loader.xlsx', var_name='poos_CPIA1s_xgbagamma0_rh_s42',
             seed=42, set_hparam=set_hparam)
