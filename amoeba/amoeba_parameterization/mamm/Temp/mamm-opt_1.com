%RWF=/home/chase/temp/Gau-mamm/,166GB
%Nosave
%Chk=mamm-opt_1.chk
%Mem=5GB
%Nproc=6
#P opt=(ModRedundant,maxcycles=400,Loose) MP2/6-31G* MaxDisk=166GB 

mamm Gaussian OPT Calculation on DESKTOP-26BCFJT

1 1
 C    0.745300   -0.057200    0.092300
 N   -0.715000    0.054900   -0.088500
 H   -1.137500   -0.858500   -0.301000
 H   -1.170900    0.416900    0.759400
 H   -0.949100    0.691500   -0.861600
 H    0.927400   -0.742500    0.922200
 H    1.168000   -0.444500   -0.836700
 H    1.131800    0.939400    0.314000

