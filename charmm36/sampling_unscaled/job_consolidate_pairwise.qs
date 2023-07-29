#!/bin/bash -l

#SBATCH --partition=idle
#SBATCH --job-name="Consol"
#SBATCH --time=0-04:00:00
#SBATCH -o %x_%j.txt
#SBATCH --export=NONE
#SBATCH --mail-user='cherman@udel.edu'
#SBATCH --mail-type=BEGIN,END,FAIL

vpkg_require python/3.8.6
cd $SLURM_SUBMIT_DIR

python get_pairwise_ener_and_dist.py 

