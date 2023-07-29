#!/bin/bash

cd w1500

vmd -dispdev text -eofexit < ../files/run_psfgen.tcl > psfgen.log

cd ../
