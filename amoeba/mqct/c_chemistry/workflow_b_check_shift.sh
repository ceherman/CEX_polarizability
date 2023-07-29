#!/bin/bash
# For future reference - the alternative strategy is just to pull the ion out of
# starting .pdb (using awk) and then delete the H atoms manually

for ion in acet esna mso4 guan imim mamm
do
    cd $ion

    cp ../check_heavy.py .
    python check_heavy.py

    cd ../
done
