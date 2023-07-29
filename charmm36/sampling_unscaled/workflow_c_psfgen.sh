#!/bin/bash

for pair in acet_guan acet_imim acet_mamm esna_guan esna_imim esna_mamm mso4_guan mso4_imim mso4_mamm
do 
    cd $pair
        
    ## Split the pdb file according to the segment
    echo REMARK > solvent.pdb
    echo REMARK > cation.pdb
    echo REMARK > anion.pdb

    awk '/SOLV/ {print}' starting.pdb >> solvent.pdb
    awk '/CION/ {print}' starting.pdb >> cation.pdb
    awk '/AION/ {print}' starting.pdb >> anion.pdb

    echo END >> solvent.pdb
    echo END >> cation.pdb
    echo END >> anion.pdb

    # Run the psfgen script
    vmd -dispdev text -eofexit < ../run_psfgen.tcl > psfgen.log

    # rm solvent.pdb cation.pdb anion.pdb

    cd ../
done


