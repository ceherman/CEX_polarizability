# #!/bin/bash
# # I modified the starting.pdb manually to add the box dimensions

# for ion in acet esna mso4 guan imim mamm
# do
#     mkdir -p $ion
#     cd $ion

#     cp ../packmol.inp .
#     cp ../../a_water_box/water.pdb .
#     cp ../../b_cavity/pdb_files/${ion}_centered.pdb ./ion.pdb
#     cp ../../b_cavity/pdb_files/${ion}_centered_heavy.pdb ./heavy.pdb

#     packmol < packmol.inp > packmol.log

#     cd ../
# done
