from numpy import *
#
# A Script to rewrite the pdb file in a way that CHARMM should like
#
import string, sys
# from Numeric import *
input = sys.argv[1]
output = input[:-4]+'.bones'
#
com = input[:-4]+'.com'
lines = map(string.split,  open(input,'r').readlines()[1:-1] )

atind = map ( string.atoi, map ( lambda line: line[1], lines ) )
atom = map ( lambda line: line[2], lines )
res = map ( lambda line: line[3], lines )
resid = map ( string.atoi, map ( lambda line: line[4], lines ) )
x = map ( string.atof, map ( lambda line: line[5], lines ) )
y = map ( string.atof, map ( lambda line: line[6], lines ) )
z = map ( string.atof, map ( lambda line: line[7], lines ) )
o = map ( string.atof, map ( lambda line: line[8], lines ) )
b = map ( string.atof, map ( lambda line: line[9], lines ) )
sg = map ( lambda line: line[10], lines ) 
# ix = map ( lambda line: line[11], lines ) 
ix = map ( lambda line: line[0], atom ) 
#
print "Finished reading data"
out = []
num = len(atom)
fmt = "%s%7d  %-3s %s%5d    %8.3f%8.3f%8.3f%6.2f%6.2f      %8.3f%2s\012" 
fmt1 = "%s%7d  %-3s %s%6d    %8.3f%8.3f%8.3f%6.2f%6.2f      %s%2s\012"
fmt2 = "%s%7d  %-3s %s%6d    %8.3f%8.3f%8.3f%6.2f%6.2f      %8.3f%2s\012"
distance=zeros(num,float)
CurrentResidue=0
numbones = 0
ghostout = []
for resindex in range(1,resid[num-1]+1):
    numbones = 0
    max = 0.0
    center = array([0.0,0.0,0.0])
    for i in range(0,num):
        if (atom[i][0]!="H" and resid[i]==resindex):
            center = center+array([x[i],y[i],z[i]])
            numbones = numbones+1
    center = center/numbones
    #
    for i in range(0,num):
        if (atom[i][0]!="H" and resid[i]==resindex):
   
           b[i] = 0.0
           o[i] = 1.0
           d = array([x[i],y[i],z[i]]) - center
           dist = sqrt(dot(d,d))
           s = fmt1 % ("ATOM",atind[i],atom[i],res[i],resid[i],x[i],y[i],z[i],o[i],b[i],"PROT",ix[i])
           if (max<=dist):
              max = dist
           out.append(s)
    s = fmt2 % ("ATOM",resindex,"G","GHO",resindex,center[0],center[1],center[2],0.00,0.00,max,"G")   
    ghostout.append(s)
open(output,'w').writelines(out)
#
open(com,'w').writelines(ghostout)
