import string, sys, os
from numpy import *
#
# cmd = "python block_averaging_replacement.py input > output" 
# cmd = "/home/dilipa/Entropy/stat_gr < input > output"
cmd = "/home/chase/codes/stat_gr < input > output"

all_out = []
fmt = "%8.3f  %10.5f  %10.5f  %10.5f\012"
fmt2 ="%1.4f"
LambdaPoints = [0.0254 , 0.1292, 0.2971, 0.5000, 0.7029, 0.8708, 0.9746]
startpoint = string.atoi(sys.argv[1])

for LambdaRange in range(startpoint,5):    
    # 
    for i in LambdaPoints:
        #
        r = string.atof(i)+LambdaRange
        #
        finp = "wbigbox_"+fmt2%(r)+".log"
        print finp 
        try:
            open(finp,'r')
            os.system("./extract_column %(finp)s" % vars() )
            #
            ftmp = map ( string.split, open('out1','r').readlines())
            y    = map ( string.atof, map ( lambda line: line[1], ftmp ))
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
            if total <> 0.0:
                Correction = -0.592 *  log ( total/nd)
            elif 1:
                Correction = 0.0
            #
            os.system("%(cmd)s " % vars())
            ftmp = map ( string.split, open('output','r').readlines())
            mean_force   = map ( string.atof, map ( lambda line: line[0], ftmp ))
            error_force  = map ( string.atof, map ( lambda line: line[1], ftmp ))    
            mf = mean_force[0]
            ef = error_force[0]
            #
        except IOError:
            #
            mf = 0
            ef = 0
            Correction = 0
        #
        s = fmt % (r,mf,ef,Correction)
        all_out.append(s)
        print s
    #
#
open('force.dat','w').writelines(all_out) 
