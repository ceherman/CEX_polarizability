#!/bin/bash

for ion in acet esna mso4
do
    cd $ion

    ## Split the pdb file according to the segment
    echo REMARK > positioned_solvent.pdb
    echo REMARK > positioned_anion.pdb

    awk '/SOLV/ {print}' starting.pdb >> positioned_solvent.pdb
    awk '/ION/ {print}' starting.pdb >> positioned_anion.pdb

    echo END >> positioned_solvent.pdb
    echo END >> positioned_anion.pdb

    # Run the psfgen script
    vmd -dispdev text -eofexit < ../files/run_psfgen_aion.tcl > psfgen.log
    
    cp positioned_anion.pdb positioned_ion.pdb # band-aid solution for b_chemistry_with_charges

    cd ../
done


for ion in guan imim mamm
do
    cd $ion

    ## Split the pdb file according to the segment
    echo REMARK > positioned_solvent.pdb
    echo REMARK > positioned_cation.pdb

    awk '/SOLV/ {print}' starting.pdb >> positioned_solvent.pdb
    awk '/ION/ {print}' starting.pdb >> positioned_cation.pdb

    echo END >> positioned_solvent.pdb
    echo END >> positioned_cation.pdb

    # Run the psfgen script
    vmd -dispdev text -eofexit < ../files/run_psfgen_cion.tcl > psfgen.log
    
    cp positioned_cation.pdb positioned_ion.pdb

    cd ../
done

