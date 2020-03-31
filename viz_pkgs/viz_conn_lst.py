"""National Modelling support statistics: 12/31/2019 created by Seonggyu Park
   last modified day: 4:31 03/27/2020 by Seonggyu Park
"""

from tqdm import tqdm
import pandas as pd
import os


def create_conn_lst(sim, net_wd=None, cha_file=None, out_fd=None, out_file=None, top_num=None):
    """create a dataframe of discrepancy for the whole watersheds

    Args:
        - sim (`list`): list of available HUC8 models
        - net_wd (`path`): path to network working directory (e.g. r'//dragonfly/NAM/Models/Default_Generated/Models')
        - cha_file (`str`): default is cha.key
        - out_fd (`path`): path to user output folder to store an excel file for the connectivity dataframe
        - out_file (`str`): excel file name
                            default is `output.xlsx`.
        - top_num (`int`): number for filtering high discrepance ranking
                            default is `5`
    Returns:
        `pandas.DataFrame`: a dataframe of discrepancy for the whole watersheds

    Example:
        from viz_pkgs.viz_conn_lst import create_conn_lst as ccl
        ccl(sim, net_wd=net_wd, out_fd=out_fd, top_num=10)
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
    if top_num is None:
        top_num = 5


    big_df = pd.DataFrame()
    for i in tqdm(sim):
        data_df = pd.read_csv(
                            os.path.join(net_wd, i, cha_file),
                            sep=r'\s+', skiprows=[0, 2], header=0, usecols=['name', 'flo_out'],
                            index_col=0)
        cha_df = pd.read_csv(
                            os.path.join(net_wd, i, cha_key),
                            sep=r'\s+', skiprows=2, header=None, usecols=[1, 2, 4, 7, 8],
                            names=['CHA_NAME', 'COMID', 'HUC12', 'DWN_OBJ', 'DWN_ID'],
                            index_col=0,
                            dtype={'HUC12': str, 'DWN_ID': str}
                            )

        df = pd.concat([cha_df, data_df], axis=1, sort=False)

        # Keep only channel or resovier down objects
        df = df[(df['DWN_OBJ'] == 'lcha') | (df['DWN_OBJ'] == 'res')]

        # Calculating received water 
        # find dwn_ids
        dwn_df = df.groupby('DWN_ID')['flo_out'].agg(['sum','count'])
        dwn_df.index.names = ['COMID']
        dwn_df.index = dwn_df.index.astype('str')

        # reset index to COMID
        df = df.reset_index()
        df = df.set_index('COMID')
        df.index.names = ['COMID']
        df.index = df.index.astype('str')

        # merge two dataframes including nan
        df = df.merge(dwn_df, on='COMID', how='outer')
        # df = pd.concat([df, dwn_df], axis=1, sort=False) # 
        df = df.dropna(subset=['index'])  # delete non lcha object
        df['DISCR_val'] = (df['flo_out'] - df['sum'])
        df['DISCR_%'] = (df['flo_out'] / df['sum']) * 100
        data_dff = df
        data_dff = data_dff.rename(columns={'index': 'CHA_NAME'})
        data_dff['DISCR_%'] = data_dff['DISCR_%'].fillna(0)

        # # data_dff = data_dff.reset_index()
        # data_dff = data_dff.rename(columns={'index': 'CHA_NAME'})
        data_dff = data_dff.iloc[(-data_dff['DISCR_%'].abs()).argsort()].iloc[:top_num]
        big_df = pd.concat([big_df, data_dff], axis=0)

    big_df.insert(1, 'HUC8', big_df['HUC12'].str[:8])
    big_df.to_excel(os.path.join(out_fd, out_file), index=True, index_label='COMID', engine='openpyxl')
    print('== Completed! ==')
    print('{} file has been exported to {} folder.'.format(out_file, out_fd))

    return big_df
