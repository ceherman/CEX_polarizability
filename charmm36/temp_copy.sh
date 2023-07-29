#!/bin/bash


# rm -r sampling_unscaled
# mkdir sampling_unscaled
# cd sampling_unscaled
# cp /home/chase/namd/ion_pairs/cgenff/brute_force_tip/* .

# for aion in acet esna mso4
# do
#     for cion in guan imim mamm
#     do
#         mkdir ${aion}_${cion}
#         rsync -r --exclude '*pair*' --exclude '*.npy' --exclude '*.dcd' --exclude '*.coor' --exclude '*core*' --exclude '*.log' /home/chase/namd/ion_pairs/cgenff/brute_force_tip/${aion}_${cion} .
#     done
# done

# cd ../


rm -r sampling_ecc
mkdir sampling_ecc
cd sampling_ecc
cp /home/chase/namd/ion_pairs/cgenff/brute_force_tip_scaled/* .

for aion in acet esna mso4
do
    for cion in guan imim mamm
    do
        mkdir ${aion}_${cion}
        rsync -r --exclude '*pair*' --exclude '*.npy' --exclude '*.dcd' --exclude '*.coor' --exclude '*core*' --exclude '*.log' /home/chase/namd/ion_pairs/cgenff/brute_force_tip_scaled/${aion}_${cion} .
    done
done

cd ../
