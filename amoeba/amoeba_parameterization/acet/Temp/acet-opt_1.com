%RWF=/home/chase/temp/Gau-acet/,166GB
%Nosave
%Chk=acet-opt_1.chk
%Mem=5GB
%Nproc=6
#P opt=(ModRedundant,maxcycles=400,Loose) MP2/6-31G* MaxDisk=166GB 

acet Gaussian OPT Calculation on DESKTOP-26BCFJT

-1 1
 C   -0.634100   -0.088100   -0.025400
 C    0.868200    0.127100    0.034000
 O    1.246500    1.324800   -0.090400
 O    1.547600   -0.924500    0.200800
 H   -1.166900    0.856600   -0.170900
 H   -0.880300   -0.755500   -0.856600
 H   -0.980900   -0.540400    0.908500

