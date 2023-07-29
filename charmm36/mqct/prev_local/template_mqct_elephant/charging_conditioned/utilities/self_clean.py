#
# Script to insert imidazolium and compute the average binding energy
#
import string, sys
#
sys.path.append('/home/arjun/Tools/MDTools/')
#
from numpy import *
import md
import kvec_new
#
# ANINT definition
#
def anint(x):
    tmp = int(x)
    diff = x - tmp
    if diff >= 0.5:
        return tmp + 1.0
    elif diff <= -0.5:
        return tmp - 1.0
    elif 1:
        return tmp
#
# ERFC
#
def erfc(x):
    z = math.fabs(x)
    t = 1.0 / ( 1.0 + 0.5*z)
    f = t*(-0.82215223 + t*0.17087277)
    f = t*( 1.48851587 + f)
    f = t*(-1.13520398 + f)
    f = t*( 0.27886807 + f)
    f = t*(-0.18628806 + f)
    f = t*( 0.09678418 + f)
    f = t*( 0.37409196 + f)
    f = t*( 1.00002368 + f)
    f = f - 1.26551223 - z*z
    v1 = t* math.exp ( f )
    if x < 0.0:
        v1 = 2.0 - v1
    return v1
#
# Details from DCD
#
fpdb = sys.argv[1]
fpsf = sys.argv[2]
mol = md.Molecule(pdb=fpdb,psf=fpsf)
#
natoms = len ( mol.coordinates() )
print "Number of atoms = ", natoms
#
boxl = string.atof ( sys.argv[3] )
eta = 5.6 / boxl
#
(nvec,rkvec,fkvec) = kvec_new.kvecs(boxl,eta,6,38)
#
#
refcoords = mol.coordinates()/boxl
refcharge = mol.charges()
#
print "Molecule monopole = ", sum(refcharge)
dipole = dot(refcharge,refcoords)*boxl
print "Molecule dipole = ", sqrt(dot(dipole,dipole))*4.8
#
# Self interaction part
#
TotalEwald = 0.0
TotalCoul = 0.0
TotalBack = 0.0
const = -pi / ( eta * eta ) / (boxl*boxl*boxl)
        
for k in range(0,natoms-1):

    SumReal = 0.0
    SumRecip = 0.0
    SumCoul = 0.0
    SumBack = 0.0
            
    wati = refcoords[k]
    qi = refcharge[k]

    for j in range(k+1,natoms):
        #
        watj = refcoords[j]
        qj = refcharge[j]
        #
        SumBack = SumBack + const * qj
        #
        # Real space sum
        #
        dx = watj - wati
        wrap = map ( anint, dx )
        dx = dx - wrap
        #
        dist = sqrt ( dot(dx,dx) ) * boxl
        #
        SumReal = erfc(eta*dist)*(qj/dist) + SumReal
        SumCoul = qj/dist + SumCoul
        # 
        # Reciprocal space sum
        #
        dx = watj - wati
        kr = dot(dx,rkvec)
        arg1 = cos(kr)
        #
        tmpsum = dot(arg1,fkvec)
        SumRecip = SumRecip + tmpsum*qj
        #
    SumRecip = 2.0*SumRecip/(boxl*pi)
    Elec = qi*(SumReal+SumRecip)*332.06
    SumBack = SumBack * qi * 332.06
    SumCoul = SumCoul * qi * 332.06
    #
    TotalEwald = TotalEwald + Elec
    TotalCoul = TotalCoul + SumCoul
    TotalBack = TotalBack + SumBack
#
print "Done with atom-atom interaction part"
print "Total Ewald contributions = ", TotalEwald
print "Total Coulomb interactions = ", TotalCoul
print "Total background contributions = ",TotalBack
#
sintr = -2.837297
SumSelf = 0.0
for j in range(0,natoms):
    qj = refcharge[j]
    SumSelf = SumSelf + qj*qj
#
SumSelf = sintr * SumSelf * 332.06 / boxl
SumSelf = SumSelf / 2.0
#
# Surface term
#
surface = zeros((3),float)
for j in range(0,natoms):
    surface = surface + refcharge[j]*refcoords[j]*boxl
#
surface_mag = dot(surface,surface)
volume = boxl * boxl * boxl
surface_term = (2*pi/volume) * surface_mag * 332.06
# print "The surface term is = ", surface_term

print "The self interaction term = ", SumSelf
#
# Correction for Ewald
#
Corr = TotalEwald + TotalBack + SumSelf - TotalCoul
print "Correction to Ewald ", Corr


