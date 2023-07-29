#!/bin/bash

for ion in acet esna mso4 guan imim mamm
do

    echo REMARK > ${ion}_centered_heavy.pdb
    awk '{if ( $1=="ATOM" && substr($3,1,1)!="H" ) print}' ${ion}_centered.pdb >> ${ion}_centered_heavy.pdb
    echo END >> ${ion}_centered_heavy.pdb

done
