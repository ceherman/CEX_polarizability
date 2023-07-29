# Reference the following for vmd command line options
# https://www.ks.uiuc.edu/Research/vmd/current/ug/node246.html

package require psfgen
topology ../toppar_c36_jul22/top_all36_cgenff.rtf
topology ../toppar_c36_jul22/ch_top_water_ions.rtf

segment AION {pdb anion.pdb}
segment CION {pdb cation.pdb}
writepsf just_solutes.psf

segment SOLV {pdb solvent.pdb}
writepsf system.psf

