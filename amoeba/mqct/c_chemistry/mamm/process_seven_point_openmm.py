import string, sys, os
from numpy import *
#
cmd = "/home/chase/codes/stat_gr < input | tee output"
all_out = []
fmt = "%8.3f  %10.5f  %10.5f  %10.5f\012"
fmt2 ="%1.4f"
LambdaPoints = [0.0254 , 0.1292, 0.2971, 0.5000, 0.7029, 0.8708, 0.9746]
startpoint = 2
endpoint = 5
count = 0
conv_factor = 1.0/10.0
for LambdaRange in range(startpoint,endpoint):    
    # 
    for i in LambdaPoints:
        #
        r = float(i)+LambdaRange
        #
        finp = 'force' + str(count) + '.dat'
        count+=1
        print(finp) 
        try:
            open(finp,'r')
            os.system("tail -n 12000 %s > out1" % finp ) # 8000
            #
            ftmp = open('out1','r').readlines()
            y    = list(map ( float, ftmp))
            y    = array((y))
            #
            nd   = len ( y )
            #
            total = 0
            for k in range(0,nd):
                #
                if y[k] == 0.0:
                    total = total + 1.0
            #
            if total != 0.0:
                Correction = -0.592 *  log ( total/nd)
            elif 1:
                Correction = 0.0
            #
            print("%(cmd)s " % vars())
            os.system("%(cmd)s " % vars())
            ftmp = open('output','r').readlines()[0]
            vals = ftmp.split()
            mf   = float(vals[0])*conv_factor
            ef  = float(vals[1])*conv_factor
            #
        except IOError:
            #
            mf = 0
            ef = 0
            Correction = 0
        #
        s = fmt % (r,mf,ef,Correction)
        all_out.append(s)
        print(s)
    #
#
open('force.dat','w').writelines(all_out) 
