#!/bin/bash

# WAS USED FROM ONE DIRECTORY ABOVE PREVIOUSLY

rsync -avS --exclude 'pair_*/' --exclude 'job_get_energies*' --exclude 'get_energies*' darwin.hpc.udel.edu:/lustre/lenhoff/users/2688/namd/brute_force_tip_scaled .

