#!/bin/bash -l

#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --job-name="xxx_ion_xxx_all"
#SBATCH --time=1-00:00:00
#SBATCH -o stdout_%j.txt
#SBATCH --export=NONE
#SBATCH --mail-user='cherman@udel.edu'
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mem=100G

vpkg_require my_py_env
cd $SLURM_SUBMIT_DIR

python make_arc_file.py all
./analyze all.arc amoebabio18_mod.prm E > all.log
python extract_frame_energies.py all.log
