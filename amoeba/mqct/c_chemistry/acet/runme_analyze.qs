#!/bin/bash -l

#SBATCH --partition=idle
#SBATCH --job-name="Forces"
#SBATCH --time=0-05:00:00
#SBATCH -o %x_%j.txt
#SBATCH --export=NONE
#SBATCH --mail-user='cherman@udel.edu'
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G

vpkg_require my_py_env
cd $SLURM_SUBMIT_DIR

python analyze_sepdcd.py
