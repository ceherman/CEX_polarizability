from numpy import *
#
#
import string, sys
#
# the file which has bones/heavy atoms 
inputbones = sys.argv[1]
#
lines = map(string.split,  open(inputbones,'r').readlines() )
resid = map ( string.atoi, map ( lambda line: line[4], lines ) )
x = map ( string.atof, map ( lambda line: line[5], lines ) )
y = map ( string.atof, map ( lambda line: line[6], lines ) )
z = map ( string.atof, map ( lambda line: line[7], lines ) )

atom = map ( lambda line: line[2], lines )
num = len(atom)

#the file which has all the center of residues

inputcom = sys.argv[2]
#
lines = map(string.split,  open(inputcom,'r').readlines() )
xcom = map ( string.atof, map ( lambda line: line[5], lines ) )
ycom = map ( string.atof, map ( lambda line: line[6], lines ) )
zcom = map ( string.atof, map ( lambda line: line[7], lines ) )
#distance
dcom = map ( string.atof, map( lambda line: line[10], lines) )

atom = map ( lambda line: line[2], lines )
numcom = len(atom)



fid=open("temp.dat","w")
fid.close()
fid=open("temp.dat","a")

#
s="set numbones "+str(num)+"\012"+"\012"
fid.write(s)
s="set numcom "+str(numcom)+"\012"+"\012"
fid.write(s)
#
s="global numcom com bones numbones"+"\012\012"
fid.write(s)
#
s="set com {}"+"\012\012"
fid.write(s)
#
s="set bones {}"+"\012\012"
fid.write(s)
#
i=1
while i <= numcom:
      si=str(i)
      xc="lappend com  "
      s="%s" %(xc)+"%7d%8.3f%8.3f%8.3f%8.3f"%(i,xcom[i-1],ycom[i-1],zcom[i-1],dcom[i-1])+"\012"
      fid.write(s)
      i=i+1
#
s="\012\012"
fid.write(s)

i=1
while i <= num:
      si=str(i)
      xc="lappend bones"
      s="%s" %(xc)+"%7d%7d%8.3f%8.3f%8.3f"%(i,resid[i-1],x[i-1],y[i-1],z[i-1])+"\012"
      fid.write(s)
      i=i+1
