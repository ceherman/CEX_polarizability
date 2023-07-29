#!/bin/bash

for anion in acet esna mso4
do
    for cation in guan imim mamm
    do
        cd ${anion}_${cation}
        echo ${anion}_${cation}
        date +"%T.%N"

        for i in {1..22}
        do
            echo $i

            for j in {23..44}
            do
                new_dir=pair_${i}_${j}
                mkdir -p $new_dir
                cd $new_dir
                echo REMARK > pair.pdb

                awk -v i=$i -v j=$j '{  if ( $1=="ATOM" && $5==i ) {
                                            print gensub (/[^[:blank:]]+/, "1.00", 9);
                                        }
                                        else if ( $1=="ATOM" && $5==j ) {
                                            print gensub (/[^[:blank:]]+/, "2.00", 9);
                                        }
                                        else if ( $1=="ATOM" ) {
                                            print gensub (/[^[:blank:]]+/, "0.00", 9)
                                        }}' ../sampling_0.coor >> pair.pdb

                echo END >> pair.pdb
                cd ../
            done
        done
        cd ../
    done
done
