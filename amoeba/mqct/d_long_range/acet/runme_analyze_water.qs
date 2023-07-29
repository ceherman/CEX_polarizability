#!/bin/bash -l

#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --job-name="acet_wat"
#SBATCH --time=1-00:00:00
#SBATCH -o stdout_%j.txt
#SBATCH --export=NONE
#SBATCH --mail-user='cherman@udel.edu'
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mem=100G

vpkg_require my_py_env
cd $SLURM_SUBMIT_DIR

python make_arc_file.py water
./analyze water.arc amoebabio18_mod.prm E > water.log
python extract_frame_energies.py water.log
