# Python 2
# python ../utilities/fix_charge.py [AION,CION] 3 system.psf
# Note:  I modified this to make segment a list input

import string, sys
from numpy import * 

segment = sys.argv[1]
print "Charges will be scaled for ", segment

scale1 = float(sys.argv[2])
print "Scale factors are: %10.5f\012" % (scale1)
scale = (scale1)
ns = 1

finp = open(sys.argv[3],'r').readlines()
numlines = len(finp)

# Let's find how many remark columns there were
numremark = string.atoi(string.split(finp[2])[0])
print "Number of remark lines = ", numremark

# Atom data then starts from
numheadskip = 2 + numremark + 2
numatoms = string.atoi(string.split(finp[numheadskip])[0])
print "Number of atoms = ", numatoms

# All atom data exists between numheadskip+1 to numheadskip+numatoms
# print finp[numheadskip+1]
# print finp[numheadskip+numatoms]
fnew = finp[numheadskip+1:numheadskip+1+numatoms]
print fnew[0]
print fnew[len(fnew)-1]
fmt = "%8d %4s %-5d%-4s %-4s %-4s%11.6f%14.4f%12d\012"

for nscales in range(0,ns):
   out = []
   if ns == 1:
      scalefactor = scale
   elif 1:
      scalefactor = scale[nscales]
   for i in range(numheadskip+1,numheadskip+1+numatoms):
      line = string.split ( finp[i] )
      index = string.atoi (line[0])
      group = line[1]
      resid = string.atoi (line[2])
      resd  = line[3]
      atom  = line[4]
      atype = line[5]
      chg   = string.atof (line[6])
      mass  = string.atof (line[7])
      move  = string.atoi (line[8])

      if group in segment:
         chg = chg * scalefactor
         s = fmt % (index,group,resid,resd,atom,atype,\
                    chg,mass,move)
         # print finp[i]
         # print s
      if group not in segment:
         out.append(finp[i])
      elif 1:
         out.append(s)

   alllines = finp[:numheadskip+1]+out+finp[numheadskip+1+numatoms:]
   # print alllines
   scale_file = "%6.4f" % (scalefactor)
   fout = "scaled_"+scale_file+".psf"
   open(fout,'w').writelines(alllines)
