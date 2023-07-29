%RWF=/home/chase/temp/Gau-mso4/,166GB
%Nosave
%Chk=mso4-opt_1.chk
%Mem=5GB
%Nproc=6
#P opt=(ModRedundant,maxcycles=400,Loose) MP2/6-31G* MaxDisk=166GB 

mso4 Gaussian OPT Calculation on DESKTOP-26BCFJT

-1 1
 S   -1.238300    0.331600    0.231700
 O   -1.536900    0.354100   -1.197700
 O   -1.365800   -0.981900    0.857300
 O    0.363400    0.637500    0.297200
 C    1.218000   -0.268900   -0.363200
 O   -1.824200    1.429100    0.994000
 H    1.004800   -0.297900   -1.435700
 H    2.249400    0.068900   -0.229400
 H    1.129500   -1.272400    0.063200

