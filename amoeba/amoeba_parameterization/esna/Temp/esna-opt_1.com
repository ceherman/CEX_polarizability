%RWF=/home/chase/temp/Gau-esna/,166GB
%Nosave
%Chk=esna-opt_1.chk
%Mem=5GB
%Nproc=6
#P opt=(ModRedundant,maxcycles=400,Loose) MP2/6-31G* MaxDisk=166GB 

esna Gaussian OPT Calculation on DESKTOP-26BCFJT

-1 1
 C   -0.097900   -0.646800   -0.061800
 C   -1.325800    0.223000    0.125400
 S    1.417400    0.285700   -0.077800
 O    1.437300    0.929600    1.233900
 O    2.432400   -0.749500   -0.266500
 O    1.250100    1.191700   -1.212300
 H   -0.022600   -1.377600    0.749800
 H   -0.157400   -1.188900   -1.011000
 H   -1.284800    0.769400    1.072800
 H   -1.419000    0.957400   -0.680800
 H   -2.229700   -0.394000    0.128400

