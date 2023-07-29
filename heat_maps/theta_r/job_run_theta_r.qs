#!/bin/bash -l

#SBATCH --partition=idle
#SBATCH --job-name="ThetaR"
#SBATCH --time=2-00:00:00
#SBATCH -o stdout_%x_%j.txt
#SBATCH --export=NONE
#SBATCH --mail-user='cherman@udel.edu'
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=100G

vpkg_require my_py_env
cd $SLURM_SUBMIT_DIR

python mod_theta_r_mdtraj.py




