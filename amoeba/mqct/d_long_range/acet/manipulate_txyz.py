import numpy as np
import copy
#########################################################################
class tmol:
    def __init__(self,natoms,maxbonds=4):
        self.natoms = natoms
        self.maxbonds = natoms
        self.atom_number = np.zeros(natoms,dtype=int)
        self.atom_name =  list()
        self.atom_type = np.zeros(natoms,dtype=int)
        self.atom_x = np.zeros(natoms,dtype=float)
        self.atom_y = np.zeros(natoms,dtype=float)
        self.atom_z = np.zeros(natoms,dtype=float)
        self.atom_bondlist = np.zeros([natoms,maxbonds],dtype=int)
#########################################################################    
def readresdiueopenmm(resdict):
    '''
    Input:  resdict: dictionary 
    Output: None
    Returns: mol: object: tinker xyz object
    for i in range(nbonds):
        bfrom[i] = int(resdict['Bond'][i]['@from']) 
        bto[i] = int(resdict['Bond'][i]['@to']) + 1
    for i in range(nbonds):
        bfrom[i] = int(resdict['Bond'][i]['@to']) + 1
        bto[i] = int(resdict['Bond'][i]['@from']) + 1
    '''
    print(resdict)
    if '@name' in resdict['Atom']:
        mol = tmol(1)
        mol.atom_number[0] = int(1)
        mol.atom_name.append(resdict['Atom']['@name'])
        mol.atom_type[0] = int(resdict['Atom']['@type']) 
        return mol
    natoms = len(resdict['Atom'])
    mol = tmol(natoms)
    
    for i in range(0,natoms):
        mol.atom_number[i] = int(i+1)
        mol.atom_name.append(resdict['Atom'][i]['@name'])
        mol.atom_type[i] = int(resdict['Atom'][i]['@type']) 

    nbonds = len(resdict['Bond'])
    bondcounter = np.zeros_like(mol.atom_number)
    for i in range(nbonds):
        bfrom = int(resdict['Bond'][i]['@from'])
        bto = int(resdict['Bond'][i]['@to']) 
        mol.atom_bondlist[bfrom,bondcounter[bfrom]] = bto + 1
        bondcounter[bfrom]+=1
        mol.atom_bondlist[bto,bondcounter[bto]] = bfrom + 1
        bondcounter[bto]+=1
    return mol
#########################################################################    
def readtxyz(fname):
    '''
    Input:  fname: string: input tinker xyz file 
    Output: None
    Returns: mol: object: tinker xyz object
    '''

    with open(fname) as f:
        lines = f.readlines()    
    natoms = int(lines[0])
    mol = tmol(natoms)
    for i in range(0,natoms):
        line = lines[i+1].split()
        mol.atom_number[i] = int(line[0])
        mol.atom_name.append(line[1])
        mol.atom_x[i] = float(line[2])
        mol.atom_y[i] = float(line[3])
        mol.atom_z[i] = float(line[4])
        mol.atom_type[i] = int(line[5]) 
        atom_nbonds = len(line) - 6 
        for j in range(atom_nbonds):
            mol.atom_bondlist[i,j] = line[6+j]
    return mol
#########################################################################
def changetypelinear(mol,nshift):
    '''
    Input:  mol: object: tinker xyz object 
            nshift: float: Shifts moltype by this number
    Output: Alters the object directly
    Returns: None
    '''
    mol.atom_type = mol.atom_type + nshift
#########################################################################
def changexyz(mol,xyz):
    '''
    Input:  mol: object: tinker xyz object 
            xyz: natoms x 3 float: array with new atom coordinates
    Output: Alters the object directly
    Returns: None
    '''
    mol.atom_x = xyz[:,0]
    mol.atom_y = xyz[:,1]
    mol.atom_z = xyz[:,2]
#########################################################################
def combinemols(mol1,mol2,shift_type2=0):
    '''
    Input:  mol1: object: tinker xyz object 1 
            mol2: object: tinker xyz object 2
            shift_type2: int: shift atom types by this number
    Output: None
    Returns: mol: object: combined tinker xyz object
    
    Combines two mol objects with atom types shifted by number shift_type2
    '''
    changetypelinear(mol2,shift_type2)
    n1 = mol1.natoms
    n2 = mol2.natoms
    mol = tmol(n1+n2)
    mol.atom_number[0:n1] = mol1.atom_number
    mol.atom_number[n1:n1+n2] = mol2.atom_number + n1
    mol.atom_name[0:n1] = mol1.atom_name
    mol.atom_name[n1:n1+n2] = mol2.atom_name
    mol.atom_x[0:n1] = mol1.atom_x
    mol.atom_x[n1:n1+n2] = mol2.atom_x
    mol.atom_y[0:n1] = mol1.atom_y
    mol.atom_y[n1:n1+n2] = mol2.atom_y
    mol.atom_z[0:n1] = mol1.atom_z
    mol.atom_z[n1:n1+n2] = mol2.atom_z
    mol.atom_type[0:n1] = mol1.atom_type
    mol.atom_type[n1:n1+n2] = mol2.atom_type
    for i in range(n1):
        nbonds = np.count_nonzero(mol1.atom_bondlist[i,:]!=0)
        for j in range(nbonds):
            mol.atom_bondlist[i,j] = mol1.atom_bondlist[i,j]
    for i in range(n2):
        nbonds = np.count_nonzero(mol2.atom_bondlist[i,:]!=0)
        for j in range(nbonds):
            mol.atom_bondlist[i+n1,j] = mol2.atom_bondlist[i,j] + n1
    return mol
#########################################################################
def writetxyzfile(fname,mol):  
    '''
    Input:  fname: string: output tinker xyz file 
            mol: object: tinker xyz object
    Output: writes tinker xyz file to fname
    Returns: None
    '''
    out = []
    s = '%6d\n' % (mol.natoms)
    out.append(s)  
    for i in range(mol.natoms):
        s = '%6d %4s  %12.6f%12.6f%12.6f%9d' % (mol.atom_number[i],mol.atom_name[i],mol.atom_x[i],mol.atom_y[i],mol.atom_z[i],mol.atom_type[i])
        out.append(s)
        nbonds = np.count_nonzero(mol.atom_bondlist[i,:]!=0)
        for j in range(nbonds):
            s = '%5d ' % mol.atom_bondlist[i,j]
            out.append(s)
        out.append('\n')
    f = open(fname, "w")
    f.writelines(out)
    f.close() 
#########################################################################
def writetxyzframe(mol):  
    '''
    Input: mol: object: tinker xyz object
    Output: None
    Returns: out: string: tinker xyz string
    '''
    out = []
    s = '%6d\n' % (mol.natoms)
    out.append(s)  
    for i in range(mol.natoms):
        s = '%6d %4s  %12.6f%12.6f%12.6f%9d' % (mol.atom_number[i],mol.atom_name[i],mol.atom_x[i],mol.atom_y[i],mol.atom_z[i],mol.atom_type[i])
        out.append(s)
        nbonds = np.count_nonzero(mol.atom_bondlist[i,:]!=0)
        for j in range(nbonds):
            s = '%5d ' % mol.atom_bondlist[i,j]
            out.append(s)
        out.append('\n')
    return out
#########################################################################
def writetarcfile(fname,mol,xyz):
    '''
    Input:  fname: string: input tinker xyz file 
            mol: object: tinker xyz object
            xyz: nframes x natoms x 3: all coordinates
    Output: None
    Returns: out: string: tinker xyz string
    '''
    f = open(fname, "w")
    nframes = len(xyz[:,0,0])
    for i in range(nframes):
        changexyz(mol,xyz[i,:,:])
        out = writetxyzframe(mol)
        f.writelines(out)
    f.close() 
#########################################################################
def main():
    mol1 = readtxyz('./txyzfiles/acet.txyz')
    mol2 = readtxyz('./txyzfiles/guan.txyz')
    mol_combined = combinemols(mol1,mol2)
    xyz = np.random.uniform(-1,1,[2,mol_combined.natoms,3])
    print(xyz)
    writetarcfile('acetguan.arc',mol_combined,xyz)

if __name__ == "__main__":
    main()
