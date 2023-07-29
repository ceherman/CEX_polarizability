#!/bin/bash
# Python 2 

eval "$(conda shell.bash hook)"
conda activate py2

results=results_self_correction.dat
rm -f $results

for ion in acet esna mso4 guan imim mamm
do
    cd $ion

    box_length=$(awk '! /#/ {print $1}' average_length.dat)
    python self_clean_local.py just_solutes.pdb just_solutes.psf $box_length > self_correction.dat

    # Extract the last number to consolidate results
    value=$(tac self_correction.dat | awk 'NF{print $NF; exit}')
    echo $ion $value | awk '{printf "%-12s%15.10f\n", $1, $2}' >> ../$results

    cd ../
done

conda deactivate
