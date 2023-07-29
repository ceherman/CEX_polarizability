#!/bin/bash -l

#SBATCH --partition=idle
#SBATCH --job-name="MsMa"
#SBATCH --gpus=1
#SBATCH --time=7-00:00:00
#SBATCH -o stdout_2_%j.txt
#SBATCH --export=NONE
#SBATCH --mail-user='cherman@udel.edu'
#SBATCH --mail-type=BEGIN,END,FAIL

vpkg_require openmm
cd $SLURM_SUBMIT_DIR

python run_sampling.py 2 6.1831 19.0169

