#!/bin/bash -l

#SBATCH --partition=idle
#SBATCH --job-name="xxx_anion_xxxxxx_cation_xxx"
#SBATCH --time=0-04:00:00
#SBATCH -o stdout_%x_%j.txt
#SBATCH --export=NONE
#SBATCH --mail-user='cherman@udel.edu'
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mem-per-cpu=16G

vpkg_require my_py_env
cd $SLURM_SUBMIT_DIR

python consolidate_charmm_pairwise_pair_pme_off.py xxx_anion_xxx xxx_cation_xxx



