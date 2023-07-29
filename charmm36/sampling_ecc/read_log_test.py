import numpy as np
import pandas as pd
import sys

def get_log_data(log_file):
    with open(log_file, mode='r') as f:
        data_list = []
        for line in f:
            if "ETITLE:" in line:
                title = line.split()
                title = title[1:]
            elif "ENERGY:" in line:
                data_vals = line.split()
                data_vals = [float(f) for f in data_vals[1:]]
                data_list.append(data_vals)
            else:
                pass
        df = pd.DataFrame(data_list, columns=title)
    return df

df = get_log_data('./acet_guan/sampling_0.log')
print(df.columns)
