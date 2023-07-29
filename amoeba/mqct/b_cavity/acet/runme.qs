#!/bin/bash -l

#SBATCH --partition=gpu-t4
#SBATCH --job-name="cav_acet"
#SBATCH --gpus=1
#SBATCH --time=3-00:00:00
#SBATCH -o stdout_%j.txt
#SBATCH --export=NONE
#SBATCH --mail-user='cherman@udel.edu'
#SBATCH --mail-type=BEGIN,END,FAIL

vpkg_require openmm
cd $SLURM_SUBMIT_DIR

python cavity.py

