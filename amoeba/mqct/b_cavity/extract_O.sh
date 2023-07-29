#!/bin/bash

echo REMARK > starting_O.pdb
awk '{if ( $1=="ATOM" && substr($3,1,1)!="H" ) print}' ../a_water_box/starting.pdb >> starting_O.pdb
echo END >> starting_O.pdb
