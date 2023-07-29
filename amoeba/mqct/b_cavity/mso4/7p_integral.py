import string, sys
from numpy import *
#
inp = map ( string.split, open(sys.argv[1],'r').readlines())
x   = map ( string.atof, map ( lambda line: line[0], inp ) )
y   = map ( string.atof, map ( lambda line: line[1], inp ) )
unc = map ( string.atof, map ( lambda line: line[2], inp ) )
x = array((x))
y = array((y))
unc = array((unc))
#
nd = len ( y )
#
# 
gauss=7
# it is a 7 point quadrature
nrange = nd/gauss
#
xr       = []
bode_tmp = []
uncertainty = []
#
#weights for a 7 point quadrature
wt = 0.5*array([0.12948,0.27971, 0.38183, 0.4180, 0.38183, 0.27971, 0.12948]) 
wt2 = wt**2
work = 0
error = 0
for i in range(0,nrange):
    #
    k = i*gauss
    force_vec = array([y[0+k],y[1+k],y[2+k],y[3+k],y[4+k],y[5+k],y[6+k]])
    unc_vec =  array([unc[0+k],unc[1+k],unc[2+k],unc[3+k],unc[4+k],unc[5+k],unc[6+k]])
    uv2 = unc_vec**2
    error = error + dot(wt2,uv2)
    work = work+dot(wt,force_vec)
    print i+1,work,sqrt(error) 
