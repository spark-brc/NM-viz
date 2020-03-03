"""SWAT-MODFLOW PEST support statistics: 12/31/2019 created by Seonggyu Park
   last modified day: 4:31 12/31/2019 by Seonggyu Park
"""

from tqdm import tqdm
import pandas as pd
import os


def create_conn_lst(sim, net_wd=None, cha_file=None, out_fd=None, out_file=None):
    """create a parameter uncertainty file from an existing *.pst file

    Args:
        - pst_file (`str`): path and name of existing *.pst file
        - unc_file (`str`): name of parameter uncertainty file
                            If `None`, then `param.unc` is used.
                            Defult is `None`.
        - sampl_n ('int'): sample number from normal distribution
                            If `None`, then `1000` is used.
                            Defult is `None`.
    Returns:
        `pandas.DataFrame`: a dataframe of log standard deviation for each parameter
        `param.unc file`

    Example:
        sm_pst_stats.create_param_unc('my.pst', 'my.unc', 2000)

    """
    sim = sim
    if net_wd is None:
        net_wd = net_wd
    if cha_file is None:
        cha_file = 'channel_sdmorph_aa.txt'

    cha_key = 'cha.key'
    if out_fd is None:
        out_fd = out_fd
    if out_file is None:
        out_file = 'output.xlsx'

    big_df = pd.DataFrame()
    for i in tqdm(sim):
        data_df = pd.read_csv(
                            os.path.join(net_wd, i, cha_file),
                            sep=r'\s+', skiprows=[0, 2], header=0, usecols=['name', 'flo_out'],
                            index_col=0)
        cha_df = pd.read_csv(
                            os.path.join(net_wd, i, cha_key),
                            sep=r'\s+', skiprows=2, header=None, usecols=[1, 2, 4, 7, 8],
                            names=['CHA_NAME','COMID', 'HUC12', 'DWN_OBJ', 'DWN_ID'],
                            index_col=0,
                            dtype={'HUC12':str}
                            )

        df = pd.concat([cha_df, data_df], axis=1, sort=False)

        # Keep only channel down objects
        df = df[df['DWN_OBJ'] == 'lcha']

        # Calculating received water 
        # find dwn_ids
        dwn_df = df.groupby('DWN_ID')['flo_out'].agg(['sum','count'])
        dwn_df.index.name = 'COMID'
        dwn_df.index = dwn_df.index.astype('int64')

        df = df.reset_index()
        df = df.set_index('COMID')
        df.index = df.index.astype('int64')

        df = pd.concat([df, dwn_df], axis=1)
        df = df.dropna(subset=['index'])  # delete non lcha objects
        df = df.fillna(0)
        df = df.drop(['DWN_OBJ', 'DWN_ID'], axis=1)
        df['DISCR'] = df['flo_out'] - df['sum']
        data_dff = df
        # data_dff.insert(0, 'CHA_NAME', df.index)
        data_dff = data_dff.astype({'count': 'int64'})
        data_dff.loc[(data_dff['count'] == 0), 'DISCR'] = 0
        # data_dff = data_dff.reset_index()
        data_dff = data_dff.rename(columns={'index': 'CHA_NAME'})
        data_dff = data_dff.iloc[(-data_dff['DISCR'].abs()).argsort()].iloc[:5]
        big_df = pd.concat([big_df, data_dff], axis=0)

    big_df.insert(1, 'HUC8', big_df['HUC12'].str[:8])
    big_df.to_excel(os.path.join(out_fd, out_file), index=True, index_label='COMID', engine='openpyxl')
    print('== Completed! ==')
    print('{} file has been exportedd to {} folder.'.format(out_file, out_fd))

    return big_df


