%RWF=/home/chase/temp/Gau-guan/,166GB
%Nosave
%Chk=guan-opt_1.chk
%Mem=5GB
%Nproc=6
#P opt=(ModRedundant,maxcycles=400,Loose) MP2/6-31G* MaxDisk=166GB 

guan Gaussian OPT Calculation on DESKTOP-26BCFJT

1 1
 N   -0.575500    1.184600   -0.170900
 C   -0.000000   -0.000000    0.000000
 N    1.291700   -0.073700    0.299500
 H    1.859900    0.757500    0.403200
 H    1.754300   -0.963800    0.434900
 N   -0.716300   -1.110900   -0.128600
 H   -1.557900    1.268400   -0.399600
 H   -0.052200    2.046100   -0.078600
 H   -1.702100   -1.082300   -0.356300
 H   -0.302000   -2.025900   -0.003600

