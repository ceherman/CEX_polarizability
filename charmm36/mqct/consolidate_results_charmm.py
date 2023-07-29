import pandas as pd
import numpy as np

df_cavity = pd.read_fwf('./e_cavity/results.dat', header=None, names=['ion', 'cavity', 'cavity_err'])

df_lr_elect = pd.read_fwf('../mqct_for_summit_tip/c_charging_conditioned/results.dat', header=None, names=['ion', 'lr_elect', 'lr_elect_err'])
df_lr_ewald_self = pd.read_fwf('../mqct_for_summit_tip/c_charging_conditioned/results_self_correction.dat', header=None, names=['ion', 'lr_ewald_self'])
df_lr_vdw = pd.read_fwf('../mqct_for_summit_tip/c_charging_conditioned/results_LR_VdW.dat', header=None, names=['ion', 'lr_vdw', 'lr_vdw_err'])

df_lr_linear = pd.read_fwf('./f_lr_linear_response/results_long_range.dat', header=None, names=['ion', 'lr_elect_vdw', 'lr_elect_vdw_err'])

df_chemistry = pd.read_fwf('../mqct_for_summit_tip/b_chemistry_with_charges/results.dat', header=None, names=['ion', 'chemistry', 'chemistry_err'])
df_chemistry['chemistry'] *= -1 # chemistry is cavity collapse, but the computation is for cavity growth

df_all = df_cavity.merge(df_lr_elect)
df_all = df_all.merge(df_lr_ewald_self)
df_all = df_all.merge(df_lr_vdw)
df_all = df_all.merge(df_lr_linear)
df_all = df_all.merge(df_chemistry)

# I'm using the less accurate linear response model in the final result to be consistent with AMOEBA
df_all['long_range'] = df_all['lr_elect_vdw'] + df_all['lr_ewald_self']
df_all['long_range_err'] = df_all['lr_elect_vdw_err']

df_all['long_range_gauss'] = df_all['lr_elect'] + df_all['lr_ewald_self'] + df_all['lr_vdw']
df_all['long_range_gauss_err'] = np.sqrt(df_all['lr_elect_err']**2 + df_all['lr_vdw_err']**2)

df_all['total'] = df_all['cavity'] + df_all['long_range'] + df_all['chemistry']
df_all['total_err'] = np.sqrt(df_all['cavity_err']**2 + df_all['long_range_err']**2 + df_all['chemistry_err']**2)

ion_names = {'acet':'Acetate', 'esna':'Ethylsulfonate', 'mso4':'Methylsulfate', 'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
for i, cont in df_all.iterrows():
    df_all.at[i, 'nice_name'] = ion_names[cont['ion']]

df_all.to_csv('./results.csv', index=False)

print(df_all)
