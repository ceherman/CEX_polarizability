# Updated block averaging implementation

import numpy as np


def split_into_blocks(data,n):
    """Function to split data into n parts
    Function returns a tuple containing the mean over blocks (mu) and the length of the block (tb)
    """
    block_length = len(data) // n
    mu = np.zeros((n),dtype='float')
    tb = block_length * 1.0
    for i in range(n-1):
        mu[i] = np.mean ( data[i*block_length:(i+1)*block_length] )
    # We will not throw out the last few pieces of data
    i = n-1
    mu[i] = np.mean ( data[i*block_length:] )
    return (mu,tb)

def return_block_variance(data):
    """ Function returns a tuple containing the length of each block (x) and the
    block variance (s).
    """
    ndata = len(data)
    Number_of_blocks = int(np.log(ndata) / np.log(2))
    # print("Initial number of blocks = ",Number_of_blocks)
    Number_of_blocks = Number_of_blocks - 2
    points_per_block = []
    for i in range(Number_of_blocks):
        nValue = int(ndata / 2**i)
        points_per_block.append(nValue)
        # print("Partition depth = ",2**i,i)
    mValue = np.mean(data)
    s_var = np.var(data)
    s = np.zeros((Number_of_blocks),dtype='float')
    x = np.zeros((Number_of_blocks),dtype='float')
    count = 0
    for N in points_per_block:
        (zz, tb) = split_into_blocks(data,N)
        s[count] = tb * np.mean ( (zz - mValue)**2 ) / s_var
        x[count] = tb
        # print(x[count], s[count])
        count += 1
    return (ndata, mValue, s_var, x,s)

def std_eom(xx):
    """Function returns statistics of correlated data"""
    (ndata, mValue, sigma_raw, x, s) = return_block_variance(xx)
    xValue = 1/x
    yValue = 1/s
    z = np.polyfit(xValue, yValue,1)

    stdev_raw = np.sqrt(sigma_raw)
    seom_raw = np.sqrt(sigma_raw / ndata)
    inefficiency = 1/z[1]
    seom = np.sqrt(sigma_raw * inefficiency / ndata)
    # print("Mean = ", mValue)
    # print("Raw variance = ", sigma_raw)
    # print("Raw standard deviation = ", stdev_raw)
    # print("Raw standard error = ", seom_raw)
    # print("Statistical inefficiency = ", inefficiency)
    # print("Corrected standard error = ", seom )
    return (mValue, sigma_raw, stdev_raw, seom_raw, inefficiency, seom)

def get_file_correlation_stats(file, column=0):
    """Convenience function to load correlated data and compute statistics"""
    all_data = np.loadtxt(file)
    if np.ndim(all_data) == 1:
        all_data = np.reshape(all_data, (len(all_data), 1))
    data = all_data[:,column]
    stats = std_eom(data)
    return stats
