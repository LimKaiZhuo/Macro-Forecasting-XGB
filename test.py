from own_package.boosting import run_testing
from own_package.poos import poos_analysis, poos_processed_data_analysis, poos_experiment, poos_model_evaluation, \
    poos_shap, poos_analysis_combining_xgb, poos_xgb_plotting_m, combine_poos_excel_results
from own_package.features_labels import read_excel_dataloader, Fl_master, Fl_ar, Fl_pca, Fl_xgb
from own_package.others import create_results_directory, create_id_dict


class A(object):  # deriving from 'object' declares A as a 'new-style-class'
    def foo(self):
        print('foo')


class B(A):
    def doo(self):
        super().foo()  # calls 'A.foo()'
        print('du')


def selector(case, **kwargs):
    if case == 1:
        run_testing()
    elif case == 2:
        excel_dir = './excel/dataset_0720/INDPRO_data_loader.xlsx'
        output = read_excel_dataloader(excel_dir=excel_dir)
        fl_master = Fl_master(x=output[0], features_names=output[1],
                              yo=output[2], labels_names=output[3],
                              y=output[4], y_names=output[5],
                              time_stamp=output[6])
        first_est_date = '1970:1'
        id = create_id_dict(var_name='IND',
                            h=[1, 3, 6, 12, 24],
                            est='rfcv',
                            model='rf',
                            model_name='rf',
                            expt='poos',
                            seed=42)
        h_store = [1, 3, 6, 12, 24]
        h_idx_store = [0, 1, 2, 3, 4]
        for h, h_idx in zip(h_store, h_idx_store):
            poos_analysis(fl_master=fl_master, h=h, h_idx=h_idx, model_mode=id['model'], est_mode=id['est'],
                          results_dir=id['results_dir'],
                          first_est_date=first_est_date,
                          save_dir=f'{id["results_dir"]}/poos_h{h}.pkl')
    elif case == 3:
        id = create_id_dict(var_name='IND',
                            h=[1, 3, 6, 12, 24],
                            est='rfcv',
                            model='rf',
                            model_name='rf',
                            expt='poos',
                            seed=42)

        first_est_date = '1970:1'
        est_dates = [f'{x}:12' for x in range(1969, 2020, 5)[:-1]]
        poos_processed_data_analysis(
            save_dir_store=[f'{id["results_dir"]}/poos_{id["model"]}_h1_analysis_results.pkl',
                            f'{id["results_dir"]}/poos_{id["model"]}_h3_analysis_results.pkl',
                            f'{id["results_dir"]}/poos_{id["model"]}_h6_analysis_results.pkl',
                            f'{id["results_dir"]}/poos_{id["model"]}_h12_analysis_results.pkl',
                            f'{id["results_dir"]}/poos_{id["model"]}_h24_analysis_results.pkl',
                            ],
            h_store=['1',
                     '3',
                     '6',
                     '12',
                     '24',
                     ],
            results_dir=id['results_dir'],
            model_full_name=id['model_full_name'], model=id['model'],
            nber_excel_dir='./excel/NBER_062020.xlsx',
            est_dates=est_dates, first_est_date=first_est_date,
            combinations=[['rw', 'll*ln'],
                          ['rw', 'llt*ln'],
                          ['rw', 'll*ln', 'llt*ln'], ])

    elif case == 3.1:
        # Combine multiple different xgb runs by averaging them. Uses the post processed of poos_h{}.pkl.
        h_store = [1, 3, 6, 12, 24]
        h_idx_store = [0, 1, 2, 3, 4]
        poos_post_dir_store = ['./results/poos_rolling/poos_IND_xgbar',
                               './results/poos_rolling/poos_IND_xgba_rs17']
        results_dir = create_results_directory('./results/poos/poos_IND_xgba_rcombined')
        with open(f'{results_dir}/dir_stores.txt', "w") as text_file:
            text_file.write(str(poos_post_dir_store))
        for h, h_idx in zip(h_store, h_idx_store):
            poos_analysis_combining_xgb(h=h, results_dir=results_dir, poos_post_dir_store=poos_post_dir_store)
    elif case == 3.2:
        # Plot information about m iteration errors for xgb. Uses the post processed of poos_h{}.pkl.
        h_store = [1, 3, 6, 12, 24]
        h_idx_store = [0, 1, 2, 3, 4]
        results_dir = './results/poos/poos_IND_xgba_rh_s42'
        for h, h_idx in zip(h_store, h_idx_store):
            poos_xgb_plotting_m(h=h, results_dir=results_dir, ssm_modes=['ll', 'll*ln'])
    elif case == 3.3:
        # Combine rmse excel together into 1 excel file
        var_name = 'IND'
        id1 = create_id_dict(var_name=var_name,
                             h=[1, 3, 6, 12, 24],
                             est='rh',
                             model='xgb',
                             model_name='xgba',
                             expt='poos',
                             seed=42)
        id2 = create_id_dict(var_name=var_name,
                             h=[1, 3, 6, 12, 24],
                             est='rfcv',
                             model='xgb',
                             model_name='xgba',
                             expt='poos',
                             seed=42)
        id3 = create_id_dict(var_name=var_name,
                             h=[1, 3, 6, 12, 24],
                             est='rh',
                             model='rf',
                             model_name='rf',
                             expt='poos',
                             seed=42)
        id4 = create_id_dict(var_name=var_name,
                             h=[1, 3, 6, 12, 24],
                             est='rfcv',
                             model='rf',
                             model_name='rf',
                             expt='poos',
                             seed=42)
        id_store = [id1, id2, id3, id4]
        excel_store = ['./results/poos/poos_IND_ar/poos_analysis_ar.xlsx',
                       './results/poos/poos_IND_pca/poos_analysis_pca.xlsx', ] + \
                      [f'{x["results_dir"]}/poos_analysis_{x["model_full_name"]}.xlsx' for x in id_store]
        name_store = ['ar', 'pca'] + [f'{x["model_name"]}({x["est"]})' for x in id_store]
        combine_poos_excel_results(excel_store=excel_store, results_dir='./results/poos/combination',
                                   name_store=name_store, expt_type='poos',
                                   selected_xgba=['oracle', 'rw', 'll*ln', 'rw+ll*ln'])
    elif case == 4:
        # Run poos experiment for ar4 or pca
        var_name = kwargs['var_name']
        excel_dir = kwargs['excel_dir']
        results_dir = create_results_directory('./results/poos/{}'.format(var_name))
        output = read_excel_dataloader(excel_dir=excel_dir)
        fl_master = Fl_master(x=output[0], features_names=output[1],
                              yo=output[2], labels_names=output[3],
                              y=output[4], y_names=output[5],
                              time_stamp=output[6])
        fl = Fl_ar(val_split=None, x=None, yo=None, y=None,
                   time_stamp=None, time_idx=None,
                   features_names=fl_master.features_names, labels_names=fl_master.labels_names,
                   y_names=fl_master.y_names)

        first_est_date = '1970:1'
        est_dates = [f'{x}:12' for x in range(1969, 2020, 5)[:-1]]

        model_mode = 'ar'
        poos_experiment(fl_master=fl_master, fl=fl, est_dates=est_dates, z_type=1, h=1, h_idx=0,
                        m_max=3, p_max=12, model_mode=model_mode, save_dir=results_dir, first_est_date=first_est_date,
                        )
        poos_experiment(fl_master=fl_master, fl=fl, est_dates=est_dates, z_type=1, h=3, h_idx=1,
                        m_max=3, p_max=12, model_mode=model_mode, save_dir=results_dir, first_est_date=first_est_date,
                        )
        poos_experiment(fl_master=fl_master, fl=fl, est_dates=est_dates, z_type=1, h=6, h_idx=2,
                        m_max=3, p_max=12, model_mode=model_mode, save_dir=results_dir, first_est_date=first_est_date,
                        )
        poos_experiment(fl_master=fl_master, fl=fl, est_dates=est_dates, z_type=1, h=12, h_idx=3,
                        m_max=3, p_max=12, model_mode=model_mode, save_dir=results_dir, first_est_date=first_est_date,
                        )
        poos_experiment(fl_master=fl_master, fl=fl, est_dates=est_dates, z_type=1, h=24, h_idx=4,
                        m_max=3, p_max=12, model_mode=model_mode, save_dir=results_dir, first_est_date=first_est_date,
                        )

        poos_processed_data_analysis(
            save_dir_store=[f'{results_dir}/poos_{model_mode}_h1_analysis_results.pkl',
                            f'{results_dir}/poos_{model_mode}_h3_analysis_results.pkl',
                            f'{results_dir}/poos_{model_mode}_h6_analysis_results.pkl',
                            f'{results_dir}/poos_{model_mode}_h12_analysis_results.pkl',
                            f'{results_dir}/poos_{model_mode}_h24_analysis_results.pkl',
                            ],
            h_store=['1',
                     '3',
                     '6',
                     '12',
                     '24',
                     ],
            results_dir=results_dir, model_full_name=model_mode, model=model_mode,
            nber_excel_dir='./excel/NBER_062020.xlsx', est_dates=est_dates, first_est_date=first_est_date)

        model_mode = 'pca'
        results_dir = create_results_directory('./results/poos/{}'.format(var_name))
        fl = Fl_pca(val_split=None, x=None, yo=None, y=None,
                    time_stamp=None, time_idx=None,
                    features_names=fl_master.features_names, labels_names=fl_master.labels_names,
                    y_names=fl_master.y_names)
        poos_experiment(fl_master=fl_master, fl=fl, est_dates=est_dates, z_type=1, h=1, h_idx=0,
                        m_max=3, p_max=12, model_mode=model_mode, save_dir=results_dir, first_est_date=first_est_date,
                        )
        poos_experiment(fl_master=fl_master, fl=fl, est_dates=est_dates, z_type=1, h=3, h_idx=1,
                        m_max=3, p_max=12, model_mode=model_mode, save_dir=results_dir, first_est_date=first_est_date,
                        )
        poos_experiment(fl_master=fl_master, fl=fl, est_dates=est_dates, z_type=1, h=6, h_idx=2,
                        m_max=3, p_max=12, model_mode=model_mode, save_dir=results_dir, first_est_date=first_est_date,
                        )
        poos_experiment(fl_master=fl_master, fl=fl, est_dates=est_dates, z_type=1, h=12, h_idx=3,
                        m_max=3, p_max=12, model_mode=model_mode, save_dir=results_dir, first_est_date=first_est_date,
                        )
        poos_experiment(fl_master=fl_master, fl=fl, est_dates=est_dates, z_type=1, h=24, h_idx=4,
                        m_max=3, p_max=12, model_mode=model_mode, save_dir=results_dir, first_est_date=first_est_date,
                        )

        poos_processed_data_analysis(
            save_dir_store=[f'{results_dir}/poos_{model_mode}_h1_analysis_results.pkl',
                            f'{results_dir}/poos_{model_mode}_h3_analysis_results.pkl',
                            f'{results_dir}/poos_{model_mode}_h6_analysis_results.pkl',
                            f'{results_dir}/poos_{model_mode}_h12_analysis_results.pkl',
                            f'{results_dir}/poos_{model_mode}_h24_analysis_results.pkl',
                            ],
            h_store=['1',
                     '3',
                     '6',
                     '12',
                     '24',
                     ],
            results_dir=results_dir,  model_full_name=model_mode, model=model_mode,
            nber_excel_dir='./excel/NBER_062020.xlsx', est_dates=est_dates, first_est_date=first_est_date)

    elif case == 5:
        # Forecast evaluation DM
        h_store = [1, 3, 6, 12, 24]

        output = read_excel_dataloader(excel_dir='./excel/dataset_0720/INDPRO_data_loader.xlsx')
        fl_master = Fl_master(x=output[0], features_names=output[1],
                              yo=output[2], labels_names=output[3],
                              y=output[4], y_names=output[5],
                              time_stamp=output[6])

        first_est_date = '1970:1'
        est_dates = [f'{x}:12' for x in range(1969, 2020, 5)[:-1]]
        var_store = {'CPIA': ['2008:11'],
                     'PAY': ['1975:3'],
                     'CMR': ['1975:1', '1980:6', '2009:2'],
                     'DPC': ['2020:3'],
                     'IND': ['1975:1', '1980:6', '2009:2'],
                     }
        var_store = {'IND': []}

        for var_name, dates in var_store.items():
            results_dir = create_results_directory(f'./results/poos/model_eval_{var_name}')
            xgb_store = [x for x in zip(
                [f'./results/poos/poos_{var_name}_xgba_rh_s42/poos_xgb_h{h}_analysis_results.pkl' for h in h_store],
                [f'./results/poos/poos_{var_name}_xgba_rfcv_s42/poos_xgb_h{h}_analysis_results.pkl' for h in h_store],
                [f'./results/poos/poos_{var_name}_rf_rh_s42/poos_rf_h{h}_analysis_results.pkl' for h in h_store],
                [f'./results/poos/poos_{var_name}_rf_rfcv_s42/poos_rf_h{h}_analysis_results.pkl' for h in h_store],
            )]
            poos_model_evaluation(fl_master=fl_master,
                                  ar_store=[f'./results/poos/poos_{var_name}_ar/poos_ar_h{h}_analysis_results.pkl' for
                                            h
                                            in h_store],
                                  pca_store=[f'./results/poos/poos_{var_name}_pca/poos_pca_h{h}_analysis_results.pkl'
                                             for h in h_store],
                                  xgb_stores=xgb_store,
                                  results_dir=results_dir,
                                  blocked_dates=dates,
                                  first_est_date=first_est_date,
                                  blocks=True,
                                  est_dates=est_dates,
                                  combinations=[['rw', 'll*ln'],
                                                ['rw', 'llt*ln'],
                                                ['rw', 'll*ln', 'llt*ln'],
                                                ]
                                  )
    elif case == 7:
        h_store = [1, 3, 6, 12, 24]
        var_name = kwargs['var_name']
        excel_dir = kwargs['excel_dir']
        results_dir = create_results_directory('./results/poos/shap_{}'.format(var_name))
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
        poos_shap(fl_master=fl_master, fl=fl_xgb,
                  xgb_store=[f'./results/poos/{var_name}/poos_h{h}.pkl' for h in h_store],
                  first_est_date=first_est_date,
                  results_dir=results_dir)


if __name__ == '__main__':
    selector(case=3.3, excel_dir='./excel/dataset_0720/INDPRO_data_loader.xlsx', var_name='poos_IND_ar')
    # selector(case=3, excel_dir='./excel/dataset2/INDPRO_data_loader.xlsx', var_name='poos_IND_ar')
