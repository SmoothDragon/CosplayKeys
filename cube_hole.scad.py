#!/usr/bin/env python

'''Salt pig combined with Super Mario Brothers pipe
'''

import solid as sd
import numpy as np


def snub_octahedron(D,d):
    ''' Snub ctahedron centered at origin
    D: Height of snub octahedron
    d: side length of the square remaining after the tip is cut off.
    '''
    cube = sd.cube(d, center=True)
    final = sd.translate([(D-d)/2,0,0])(cube)
    final += sd.translate([-(D-d)/2,0,0])(cube)
    final += sd.rotate([0,0,90])(final)
    final += sd.rotate([90,0,0])(final)
    final = sd.hull()(final)
    return final


if __name__ == '__main__':
    fn = 32
    side = 50
    snub = side/10

    final = sd.cube(side, center=True)
    cutter = sd.rotate([45,180/np.pi*np.arcsin(1/np.sqrt(3)),0])(final)
    cutter -= sd.cube([side,side,2*side], center=True)
    # cutter = sd.intersection()(cutter, sd.cube([side,side,side], center=True))
    
    final = cutter
    final = sd.scad_render(final, file_header=f'$fn={fn};')
    print(final)


