#!/bin/bash

# Variable assignment ###############################################

# Input parameter (read from command line)
ion=$1

# Assign variables used in generating the wbigbox .namd fles
MasterRadius=0.0
RadiusPrevious_p=$MasterRadius
RadiusPrevious_m=$MasterRadius

K=5.0
Rate=0.001
RadiusDelta=0.1
Sigma=3.165492
Epsilon=0.155425

templateDir=./
template=wbigbox_template.namd
MasterDir=.
file_master=wbigbox_0.0
file=wbigbox

coordinates=$MasterDir/$file_master.coor
coordinates_p=$MasterDir/$file_master.pdb
coordinates_m=$MasterDir/$file_master.pdb

extendedsystem=$MasterDir/$file_master.restart.xsc
bin_coordinates=$MasterDir/$file_master.restart.coor
bin_velocities=$MasterDir/$file_master.restart.vel

# Quadrature rules
z1="-0.94911 -0.74153 -0.40585 0.0 0.40585 0.74153 0.94911"
# z1="-0.90618 -0.53847  0.0  0.53847 0.90618"
# z2="-0.77460   0.0  0.77460"


# First radial point ###############################################

# Generate .namd file
radius=$MasterRadius
input=$file"_"$radius.namd
output=$file"_"$radius.log
echo $radius $input

echo "set JobId" $radius                   >  $input
echo "set xsc_file" $extendedsystem        >> $input
echo "set bin_vel_file" $bin_velocities    >> $input
echo "set bin_coord_file" $bin_coordinates >> $input
echo "set coord_file" $coordinates         >> $input
echo "set rs 0"                            >> $input
cat $templateDir/$template                 >> $input
echo "tclBCArgs {$radius $radius $Rate $Sigma $Epsilon}" >> $input

# Generate .qs file for the single radial point
runme_file=runme_${radius}.qs

echo "#!/bin/bash -l
#SBATCH --nodes=1
#SBATCH --job-name=${ion}_${radius}
#SBATCH --partition=gpu-t4
#SBATCH --gpus=1
#SBATCH --time=0-01:00:00
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err
# SBATCH --mail-user='cherman@udel.edu'
# SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=NONE
#UD_QUIET_JOB_SETUP=YES
#job_exit_handler() {
#  # Copy all our output files back to the original job directory:
#  cp * \"\$SLURM_SUBMIT_DIR\"
#
#  # Don't call again on EXIT signal, please:
#  trap - EXIT
#  exit 0
#}
#export UD_JOB_EXIT_FN=job_exit_handler
#export UD_JOB_EXIT_FN_SIGNALS=\"SIGTERM EXIT\"
#UD_PREFER_MEM_PER_CPU=YES
#UD_REQUIRE_MEM_PER_CPU=YES
vpkg_require namd/2.14:nvidia
#UD_USE_SRUN_LAUNCHER=YES
#UD_DISABLE_CPU_AFFINITY=YES
#UD_MPI_RANK_DISTRIB_BY=CORE
#UD_DISABLE_IB_INTERFACES=YES
#UD_SHOW_MPI_DEBUGGING=YES
. /opt/shared/slurm/templates/libexec/openmpi.sh

\${UD_MPIRUN} namd2 +idlepoll +p\${SLURM_CPUS_ON_NODE} +devices \${CUDA_VISIBLE_DEVICES} ${input} > ${output}
mpi_rc=\$?
exit \$mpi_rc
" > $runme_file


# Create the .sh file that coordinates dependency execution across all radial points
dep_file=dep_file_jbs.sh

echo "#!/bin/bash" > $dep_file
echo "out_text=\`sbatch $runme_file\`" >> $dep_file
echo "id_p=\`echo \$out_text | awk '{print \$NF}'\`" >> $dep_file


# Assign variables to be used in the iterative loop below
bin_coordinates_p=$file"_"$radius.restart.coor
bin_velocities_p=$file"_"$radius.restart.vel
extendedsystem_p=$file"_"$radius.restart.xsc


# Other radial points ##############################################

OldRadius=$MasterRadius
for i in {0..4}
do
    NextRadius=$(echo " ( 1.0 + $OldRadius )" | bc -l) 
    dr=$(echo " ($NextRadius - $OldRadius)" | bc -l)

    if [ $i -eq  1 ]; then
        gausspoints=$z1
    else 
        gausspoints=$z1
    fi 

    for z in `echo $gausspoints`
    do
        radius_p=$(echo " ( 0.5 * $z * $dr + 0.5 * ($NextRadius+$OldRadius))" | bc -l)
        radius_print=` printf "%6.4f\n" $(echo " ( 0.5 * $z * $dr + 0.5 * ($NextRadius+$OldRadius))" | bc -l) `

        # Generate .namd file
        input_p=$file"_"$radius_print.namd
        output_p=$file"_"$radius_print.log
        echo $radius_p $input_p

        echo "set JobId" $radius_print               >  $input_p
        echo "set xsc_file" $extendedsystem_p        >> $input_p
        echo "set bin_vel_file" $bin_velocities_p    >> $input_p
        echo "set bin_coord_file" $bin_coordinates_p >> $input_p
        echo "set coord_file" $coordinates           >> $input_p
        echo "set rs 1"                              >> $input_p
        cat $templateDir/$template                   >> $input_p
        echo "tclBCArgs {$MasterRadius $radius_p $Rate $Sigma $Epsilon}" >> $input_p

        # Generate .qs file for the single radial point
        runme_file=runme_${radius_print}.qs

        echo "#!/bin/bash -l
#SBATCH --nodes=1
#SBATCH --job-name=${ion}_${radius_print}
#SBATCH --partition=gpu-t4
#SBATCH --gpus=1
#SBATCH --time=0-01:00:00
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err
# SBATCH --mail-user='cherman@udel.edu'
# SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=NONE
#UD_QUIET_JOB_SETUP=YES
#job_exit_handler() {
#  # Copy all our output files back to the original job directory:
#  cp * \"\$SLURM_SUBMIT_DIR\"
#
#  # Don't call again on EXIT signal, please:
#  trap - EXIT
#  exit 0
#}
#export UD_JOB_EXIT_FN=job_exit_handler
#export UD_JOB_EXIT_FN_SIGNALS=\"SIGTERM EXIT\"
#UD_PREFER_MEM_PER_CPU=YES
#UD_REQUIRE_MEM_PER_CPU=YES
vpkg_require namd/2.14:nvidia
#UD_USE_SRUN_LAUNCHER=YES
#UD_DISABLE_CPU_AFFINITY=YES
#UD_MPI_RANK_DISTRIB_BY=CORE
#UD_DISABLE_IB_INTERFACES=YES
#UD_SHOW_MPI_DEBUGGING=YES
. /opt/shared/slurm/templates/libexec/openmpi.sh

\${UD_MPIRUN} namd2 +idlepoll +p\${SLURM_CPUS_ON_NODE} +devices \${CUDA_VISIBLE_DEVICES} ${input_p} > ${output_p}
mpi_rc=\$?
exit \$mpi_rc
" > $runme_file

        # Append to the .sh file that coordinates dependency execution
        echo "out_text=\`sbatch -d afterok:\${id_p} $runme_file\`" >> $dep_file
        echo "id_p=\`echo \$out_text | awk '{print \$NF}'\`" >> $dep_file

        # Update loop variables
        MasterRadius=$radius_p
        bin_coordinates_p=$file"_"$radius_print.restart.coor
        bin_velocities_p=$file"_"$radius_print.restart.vel
        extendedsystem_p=$file"_"$radius_print.restart.xsc
    done

    # reset starting frame etc
    OldRadius=$NextRadius
done


