#!/bin/bash
# To be run locally

results=results_long_range.dat
rm -f $results

results_other_info=results_other_info.dat
rm -f $results_other_info

for ion in acet esna mso4 guan imim mamm
do
    cd $ion

    ln -sf ../get_long_range_energies.py .
    ln -sf ../block_averaging_functions.py .
    python get_long_range_energies.py $ion

    last_line=$(cat results.dat)
    echo $ion $last_line | awk '{printf "%-12s%15.10f%20.12f\n", $1, $2, $3}' >> ../${results}

    last_line=$(cat results_other_info.dat)
    echo $ion $last_line | awk '{printf "%-12s%20.12f%20.12f%20.12f\n", $1, $2, $3, $4}' >> ../${results_other_info}

    cd ../
done
