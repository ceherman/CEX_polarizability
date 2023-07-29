############################################################################
##### We have finished reading and assigning the atom centers of the protein
##### around which we will draw spheres. We have also read the corresponding 
##### centers of the residues. Now we will read the indices of the solvent 
##### molecules on which we will apply forces.
############################################################################

set atomID 1   ;# in NAMD, atom IDs are 1-based numbers

set inStream [open $pdbSource r]        ;# opening the PDB file

set NatomsFound 0
# reading the PDB file line after line:
foreach line [split [read $inStream] \n] {
    # symbols 0-3 should be ATOM or HETA
    set string1 [string range $line 0 3]

    # symbols 17-20 contain the residue name
    set string2 [string range $line 76 78]

    set string2 [string trim $string2] ;# trimming the residue name

    set beta [string trim [string range $line 60 65]]

    if { [string equal $string1 {ATOM}] || \
             [string equal $string1 {HETA}] } {

        # so it's a valid atom entry; let's see if this is an ion

        # if { [string equal $string2 {O}] }
        if { [string equal $beta {1.00}] } {

            # yes it's an ion; append its index to the list
            set NatomsFound [expr { $NatomsFound + 1 }]
            set OMap($atomID) 1
        } else {

            set OMap($atomID) 0

        }

        # increase the atomID counter by 1 (this is the default increment)
        incr atomID
    }
}

#for {set n 1} {$n<$atomID} {incr n} {
#    print " atomid $n $OMap($n)"
#}
print "Found $NatomsFound oxygens"
close $inStream

#####################################################################

wrapmode cell



#The following line is useless for a multiple cavity code. It 
# was present on the single cavity application of the bubble script.
foreach { x0 y0 z0 } $bubbleCenter { break }
#

set TOL 4. ;# distance tolerance parameter
set TWO_ROOT6 1.12246204830937;
#
proc calcforces {step unique StartRadius CavityRadius Rrate Sigma Epsilon} {

  global x0 y0 z0 TOL OMap TWO_ROOT6
  global bones numbones com numcom
  # numbones is number of bones
  # numcom is the number of centers of mass

  # Initiliaze the forces on every bone 
  for {set bonecount 1} {$bonecount<=$numbones} {incr bonecount} {
       set forceon($bonecount) 0.0
       }
  #
  # Set the radius of the sphere around every bone
  set R [expr {$Rrate * $step + $StartRadius}]
  if { $Rrate > 0.0 } {
      if { $R > $CavityRadius } { set R $CavityRadius }
  } else {
      if { $R < $CavityRadius } { set R $CavityRadius }
  }
  #
  #
  
  set Lambda [expr { $R - $Sigma * $TWO_ROOT6 }]

  if { $unique && $step % 1000 == 0 } {
      print "step $step, bubble radius = $R, lambda = $Lambda"
  }

  # Atoms found at a distance larger than $TOL from the surface
  # of the bubble, or $RTOL from the center of the bubble, will
  # be ignored (dropped) for the rest of a 10-step cycle.

  set RTOL [expr {$R + $TOL}]

  # restore the complete list of atoms to consider:

  if { $step % 10 == 0 } { cleardrops }


  # nextatom is the magic NAMD-tcl interface command. 
  # 
  while {[nextatom]} {

      set atomid [getid] ;# get the ID of the current atom

      # check if this ID is listed in ionList; if it's found,
      # lsearch will return the position of the search pattern
      # in the list (a number >= 0), otherwise -1 is returned

      if { $OMap($atomid) == 1 } {
          # rvec is the co-ordinate of solvent atom
          set rvec [getcoord]
          # x,y,z are co-ordinates of solvent atom
          foreach { x y z } $rvec { break }

          # Initialize the minimum distance of this solvent 
          # molecule from the surface of all the spheres.
          # rho is this minimum distance
          set rho [expr {$RTOL+$TOL}]
          # 
          # First Calculate distances of this sovent atome 
          # from all the centers of mass.
          # comcount is residue number
          # xcom,ycom,zcom are the co-ordinates of center of mass. tempdistance is 
          # the maximum distance of any atom of the residue from its center of mass.
               foreach { residuenumber xcom ycom zcom tempdistance} $com {
               set mindistfrom($residuenumber) [expr {-$tempdistance+sqrt(($x-$xcom)*($x-$xcom) + ($y-$ycom)*($y-$ycom) + \
                                  ($z-$zcom)*($z-$zcom))}]
               # minimum possible distance of this solvent molecule
               # from any heavy atom of this residue is mindistfrom
               #
               #
               # Now see if this solvent atom can be dropped becuase it is too far away from the 
               # surface of the residue.
               if { $mindistfrom($residuenumber) < $rho } {set rho  [expr {$mindistfrom($residuenumber)} ]} 
              }
         
          #Now go through all the bones

               foreach {bonecount residuenumber xbone ybone zbone} $bones { 
               if {$mindistfrom($residuenumber) <=$R} {
                   set rhobone [expr {sqrt(($x-$xbone)*($x-$xbone) + ($y-$ybone)*($y-$ybone) + \
                                  ($z-$zbone)*($z-$zbone))}]
                   if { $rhobone< $R } {
                        set frac  [expr { $Sigma / ( $rhobone - $Lambda ) } ]
                        set frac3 [expr { $frac * $frac * $frac } ]
                        set frac6 [expr { $frac3 * $frac3 } ]
                        set frac7 [expr { $frac6 * $frac } ]
                        set dVdr  [expr { 24.0 * ( $Epsilon / $Sigma ) * $frac7 * ( -2.0 * $frac6 + 1.0 ) } ]
                        set dVdl  [expr { -$dVdr } ]
                        set forceX [expr { -$dVdr * ($x-$xbone) / $rhobone } ]
                        set forceY [expr { -$dVdr * ($y-$ybone) / $rhobone } ]
                        set forceZ [expr { -$dVdr * ($z-$zbone) / $rhobone } ]
                        addforce "$forceX $forceY $forceZ"
                        addenergy "$dVdl"
                        set forceon($bonecount)  [expr {$forceon($bonecount) + $dVdl}]
                      }
                   }
                 }
          if { $rho > $RTOL } { dropatom }
          }  else {

          # no need to keep this atom
          dropatom
      }
      }

      if { $step % 250 ==0} {
      set bonecount 1
      while {$bonecount  <=$numbones} {
      print "Center $bonecount $forceon($bonecount) Step: $step"
      incr bonecount }
}
}
