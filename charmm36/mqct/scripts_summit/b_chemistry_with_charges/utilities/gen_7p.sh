#!/bin/bash

# Variable assignment ###############################################

# Input parameter (read from command line)
ion=$1

# Assign variables used in generating the wbigbox .namd fles
MasterRadius=2.0
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

# Generate .lsf file for the single radial point
runme_file=runme_${radius}.lsf

echo "#!/bin/bash
#BSUB -P GEN006
#BSUB -W 01:00
#BSUB -nnodes 1
#BSUB -alloc_flags \"gpumps smt1\"
#BSUB -J chem_${ion}_${radius}
#BSUB -e %J.err
#BSUB -o %J.out

module unload xl
module load ums/default
module load ums-gen119/default
module load namd/2.14-gcc

jsrun --bind rs -r1 -g1 -c42 namd2 +ignoresharing +ppn 41 ${input} > ${output}" > $runme_file


# Create the .sh file that coordinates dependency execution across all radial points
dep_file=dep_file_jbs.sh

echo "out_text=\`bsub $runme_file\`" > $dep_file
echo "id_p=\`echo \$out_text | awk -F\"<\" '{print \$2}'|awk -F\">\" '{print \$1}'\`" >> $dep_file


# Assign variables to be used in the iterative loop below
bin_coordinates_p=$file"_"$radius.restart.coor
bin_velocities_p=$file"_"$radius.restart.vel
extendedsystem_p=$file"_"$radius.restart.xsc


# Other radial points ##############################################

OldRadius=$MasterRadius
for i in {0..2}
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

        # Generate .lsf file for the single radial point
        runme_file=runme_${radius_print}.lsf

        echo "#!/bin/bash
#BSUB -P GEN006
#BSUB -W 01:00
#BSUB -nnodes 1
#BSUB -alloc_flags \"gpumps smt1\"
#BSUB -J chem_${ion}_${radius_print}
#BSUB -e %J.err
#BSUB -o %J.out

module unload xl
module load ums/default
module load ums-gen119/default
module load namd/2.14-gcc

jsrun --bind rs -r1 -g1 -c42 namd2 +ignoresharing +ppn 41 ${input_p} > ${output_p}" > $runme_file

        # Append to the .sh file that coordinates dependency execution
        echo "out_text=\`bsub -w \"done(\$id_p)\" $runme_file\`" >> $dep_file
        echo "id_p=\`echo \$out_text | awk -F\"<\" '{print \$2}'|awk -F\">\" '{print \$1}'\`" >> $dep_file

        # Update loop variables
        MasterRadius=$radius_p
        bin_coordinates_p=$file"_"$radius_print.restart.coor
        bin_velocities_p=$file"_"$radius_print.restart.vel
        extendedsystem_p=$file"_"$radius_print.restart.xsc
    done

    # reset starting frame etc
    OldRadius=$NextRadius
done


