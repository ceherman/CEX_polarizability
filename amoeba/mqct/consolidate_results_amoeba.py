import pandas as pd
import numpy as np

df_cavity = pd.read_fwf('./b_cavity/results.dat', header=None, names=['ion', 'cavity', 'cavity_err'])

df_chemistry = pd.read_fwf('./c_chemistry/results.dat', header=None, names=['ion', 'chemistry', 'chemistry_err'])
df_chemistry['chemistry'] *= -1 # chemistry is cavity collapse, but the computation is for cavity growth

df_lr_elect_vdw = pd.read_fwf('./d_long_range/results_long_range.dat', header=None, names=['ion', 'lr_elect_vdw', 'lr_elect_vdw_err'])
df_lr_ewald_self = pd.read_fwf('./d_long_range/results_self_correction.dat', header=None, names=['ion', 'lr_ewald_self'])

df_all = df_cavity.merge(df_chemistry)
df_all = df_all.merge(df_lr_elect_vdw)
df_all = df_all.merge(df_lr_ewald_self)

df_all['long_range'] = df_all['lr_elect_vdw'] + df_all['lr_ewald_self']
df_all['long_range_err'] = df_all['lr_elect_vdw_err']

df_all['total'] = df_all['cavity'] + df_all['long_range'] + df_all['chemistry']
df_all['total_err'] = np.sqrt(df_all['cavity_err']**2 + df_all['long_range_err']**2 + df_all['chemistry_err']**2)

ion_names = {'acet':'Acetate', 'esna':'Ethylsulfonate', 'mso4':'Methylsulfate', 'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
for i, cont in df_all.iterrows():
    df_all.at[i, 'nice_name'] = ion_names[cont['ion']]

df_all.to_csv('./results.csv', index=False)
