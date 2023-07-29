# I modified this file to use numpy instead of Numeric
# (the python interpreter on Ananda wasn't finding Numeric for me)

import string, sys
import numpy as np

#**
# This one is specific for the charging calculations, hence no x
#
inp = map ( string.split, open(sys.argv[1],'r').readlines())
x   = map ( string.atof, map ( lambda line: line[0], inp ) )
y   = map ( string.atof, map ( lambda line: line[0], inp ) )
unc = map ( string.atof, map ( lambda line: line[1], inp ) )
x = np.array((x))
y = np.array((y))
unc = np.array((unc))
#*
nd = len ( y )
#
# 
gauss=3
# it is a three point quadrature
nrange = nd/gauss
#
xr       = []
bode_tmp = []
uncertainty = []
#
#weights for a three point quadrature
wt = 0.5*np.array([5.0/9.0,8.0/9.0,5.0/9.0])
wt2 = wt**2
work = 0
error = 0
for i in range(0,nrange):
    #
    k = i*gauss
    force_vec = np.array([y[0+k],y[1+k],y[2+k]])
    unc_vec =  np.array([unc[0+k],unc[1+k],unc[2+k]])
    uv2 = unc_vec**2
    error = error + np.dot(wt2,uv2)
    work = work+np.dot(wt,force_vec)
    print i+1,work,np.sqrt(error) 
