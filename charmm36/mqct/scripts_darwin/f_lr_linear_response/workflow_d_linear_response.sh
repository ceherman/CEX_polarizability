#!/bin/bash

results=results_long_range.dat
rm -f $results

results_other_info=results_other_info.dat
rm -f $results_other_info

results_vdw=results_long_range_vdw.dat
rm -f $results_vdw

results_elect=results_long_range_elect.dat
rm -f $results_elect

results_cov=results_long_range_elect_vdw_cov.dat
rm -f $results_cov

for ion in acet esna mso4 guan imim mamm
do
    cd $ion

    # time step, electrostatic, vdw
    egrep '^ENERGY:' get_energy.log | awk '{printf("%d %f %f\n",$2,$7,$8)}' | tail -n 9000 > energies.txt

    ln -sf ../utilities/get_long_range_energies.py .
    python get_long_range_energies.py

    last_line=$(cat results_total.dat)
    echo $ion $last_line | awk '{printf "%-12s%15.10f%20.12f\n", $1, $2, $3}' >> ../${results}

    last_line=$(cat results_total_other_info.dat)
    echo $ion $last_line | awk '{printf "%-12s%20.12f%20.12f%20.12f\n", $1, $2, $3, $4}' >> ../${results_other_info}

    last_line=$(cat results_vdw.dat)
    echo $ion $last_line | awk '{printf "%-12s%15.10f%20.12f\n", $1, $2, $3}' >> ../${results_vdw}

    last_line=$(cat results_elect.dat)
    echo $ion $last_line | awk '{printf "%-12s%15.10f%20.12f\n", $1, $2, $3}' >> ../${results_elect}

    last_line=$(cat results_covariance.dat)
    echo $ion $last_line | awk '{printf "%-12s%15.10f\n", $1, $2}' >> ../${results_cov}

    cd ../
done
