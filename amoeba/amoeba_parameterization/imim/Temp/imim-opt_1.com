%RWF=/home/chase/temp/Gau-imim/,166GB
%Nosave
%Chk=imim-opt_1.chk
%Mem=5GB
%Nproc=6
#P opt=(ModRedundant,maxcycles=400,Loose) MP2/6-31G* MaxDisk=166GB 

imim Gaussian OPT Calculation on DESKTOP-26BCFJT

1 1
 N    0.590700   -0.957200    0.016100
 C    1.082800    0.248900    0.315400
 N    0.064400    1.107800    0.207100
 H    0.139500    2.109200    0.377200
 C   -1.087800    0.447900   -0.164000
 C   -0.751700   -0.870800   -0.285900
 H    1.139500   -1.815100    0.014400
 H    2.104500    0.483800    0.591200
 H   -1.995000    1.012400   -0.291100
 H   -1.286800   -1.766900   -0.548100

