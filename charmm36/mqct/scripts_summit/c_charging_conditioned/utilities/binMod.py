import string, math, sys
from numpy import *
#
def int(x):
    tmp = str ( math.floor(x) )
    return string.atoi( tmp[:-2] )
#
# Main processing segment
#
inp          = map ( string.split, open ( sys.argv[1],'r').readlines() )
column_index = string.atoi ( sys.argv[2] )
pdata        = map ( string.atof, map ( lambda line: line[column_index], inp ) )

pdata        = array((pdata))
# pdata        = sort(pdata)
#
nd = len(pdata)
# low          = pdata[0]
# high         = pdata[nd-1]
# 
avg_eng = mean ( pdata )
std_eng = std ( pdata)
print "Average = ", avg_eng
print "Standard deviation = ", std_eng
# print "Lowest  value found ", low
# print "Highest value found ", high
#
temperature = string.atof(sys.argv[3]) 
kT = 0.592 * temperature / 298.0
F_or_I = sys.argv[4]
#
blocklength = int(nd/5)
print "Block length is ", blocklength
fv = zeros((5),float)
#
for iblock in range(0,5):
    begin = iblock * blocklength
    end = begin + blocklength
    ptmp = pdata[begin:end]
    avg_eng = mean ( ptmp ) 
    std_end = std ( ptmp ) 
    pvalues = ptmp - avg_eng
    if F_or_I == "F":
        pvalues = exp(-pvalues / kT)
        fe = avg_eng - std_eng * std_eng / (2.0 * kT)
    elif F_or_I == "I":
        pvalues = exp(pvalues / kT)
        fe = avg_eng + std_eng * std_eng / (2.0 * kT)
    #
    fv[iblock] = fe
#
print mean(fv)
print std(fv)/sqrt(5-1)
