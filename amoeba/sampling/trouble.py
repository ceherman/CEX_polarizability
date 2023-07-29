import numpy as np
import pandas as pd

df_gr = pd.read_csv('./results_Ka_gr.csv')
df_c_1 = pd.read_csv('./results_Ka_counting_difference_for_unassociated.csv')
df_c_2 = pd.read_csv('./results_Ka_counting_direct.csv')
# df_c_pratt = pd.read_csv('./results_Ka_counting_pratt.csv')

# print(df_c_1['Ka_M-1']/df_gr['Ka_M-1'])
# print('')
# print(df_c_2['Ka_M-1']/df_gr['Ka_M-1'])
# print(df_c_1.p_bound - df_c_1.p_bound_from_Ka)
# print(df_c_2.p_bound - df_c_2.p_bound_from_Ka)
# print(df_c_1.p_bound - df_c_2.p_bound) # p_bound is the same

print(df_gr.head())
# print(df_c_pratt)
