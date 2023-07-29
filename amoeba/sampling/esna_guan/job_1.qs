#!/bin/bash -l

#SBATCH --partition=gpu-t4
#SBATCH --job-name="EsGu"
#SBATCH --gpus=1
#SBATCH --time=4-00:00:00
#SBATCH -o stdout_1_%j.txt
#SBATCH --export=NONE
#SBATCH --mail-user='cherman@udel.edu'
#SBATCH --mail-type=BEGIN,END,FAIL

vpkg_require openmm
cd $SLURM_SUBMIT_DIR

python run_sampling.py 1 10.0 0.2

