Workflow________________________________________________________________________

Prerequisite (only for cavity contributions)
0. Equilibration of a neat water box (with wbox_equilibrate)

Requires manual input with CHARMM GUI
1. Parameterization

Requires Packmol + VMD + Psfgen
2. ABF - manually assess PMF convergence before proceeding with conformers
(This is where my run MQCT script starts)
3. Equilibration of water box with fixed solutes

Essential MQCT - only requires NAMD
4. Chemistry - with charges
5. Charging - conditioned
6. Cavity
7. Direct interaction

Nonessential MQCT (for checking charging consistency) - only requires NAMD
8. Chemistry - without charges
9. Charging - unconditined


Workflow dependency chart_______________________________________________________

Parameterization > ABF (to get conformers)
    > Direct interaction
    > Cavity
    > Equilibrate water box with solutes fixed
        > Chemistry - with charges
            > Charging - conditioned
        > Chemistry - without charges
        > Charging - unconditioned

Notes___________________________________________________________________________

ABF - all systems have been run to 45 ns except for acet_trea 
(I need to check the trea structure and parameterization, since it's a novel ligand)

MQCT
    esna_mamm - completed with separated_xi_max
    mso4_mamm - completed with separated_xi_max - separated failed consistency
    separated conformers for these pairs were renamed _2

    -- changed from using xi_max to 15 A (where all PMF profiles seem to be
       about the same --

    Need to run all separated and (pmf_min for all but the two pairs above)

Started second esna/mso4-mamm associated conformers as _3
