#!/usr/bin/env python

'''Salt pig combined with Super Mario Brothers pipe
'''

import solid as sd
import numpy as np



if __name__ == '__main__':
    fn = 32
    side = 50
    snub = side/10

    final = sd.cube(side, center=True)
    cutter = sd.rotate([45,180/np.pi*np.arcsin(1/np.sqrt(3)),0])(final)
    cutter = sd.intersection()(cutter, sd.cube([2*side,2*side,side], center=True))
    cutter += sd.cube([side+1.2,side+1.2,side], center=True)
    cutter = sd.rotate([0,-180/np.pi*np.arcsin(1/np.sqrt(3)),0])(cutter)
    cutter = sd.rotate([-45,0,0])(cutter)
    final = sd.translate([0, side, 0])(final)
    final -= cutter
    final = sd.translate([side, -side, 0])(final)
    final = sd.rotate([0,0,180])(final)
    final -= cutter

    # cutter -= sd.cube([side,side,2*side], center=True)
    
    # final = cutter
    final = sd.scad_render(final, file_header=f'$fn={fn};')
    print(final)


