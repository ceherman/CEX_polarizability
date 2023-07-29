import MDAnalysis as mda
import json
# I know this isn't good practice...
import warnings
warnings.filterwarnings("ignore")

pdb_to_xyz_mapping = {}
for ion in ['acet', 'esna', 'mso4', 'guan', 'imim', 'mamm']:
    xyz = mda.Universe(f'{ion}.txyz')
    pdb = mda.Universe(f'{ion}.pdb')
    xyz_atoms = [atom.name for atom in xyz.atoms]
    pdb_atoms = [atom.name for atom in pdb.atoms]
    mapping = [pdb_atoms.index(atom_name) for atom_name in xyz_atoms]
    pdb_to_xyz_mapping[ion] = mapping

with open("pdb_to_xyz_index_map.json", "w") as outfile:
    json.dump(pdb_to_xyz_mapping, outfile)
