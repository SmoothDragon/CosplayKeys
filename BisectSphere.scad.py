#!/usr/bin/env python

'''Salt pig combined with Super Mario Brothers pipe
'''

import solid as sd
import numpy as np


if __name__ == '__main__':
    fn = 64
    d_ball = 100


    cutter = sd.square(d_ball, center=True)
    cutter = sd.rotate(-45)(cutter)
    cutter = sd.intersection()(cutter,
            sd.translate([d_ball,0])(sd.square(2*d_ball, center=True)))
    cutter = sd.rotate_extrude(360)(cutter)
    cutter = sd.translate([0,0,d_ball*2**-.5])(cutter)
    cutter = sd.union()(*[sd.rotate([180*i/fn,0,0])(cutter) for i in range(fn+1)])

    final = sd.sphere(d=d_ball)
    final -= cutter
    final -= sd.sphere(d=d_ball*.9)
    upper = sd.cube(d_ball*4, center=True)
    upper = sd.translate([0,0,2*d_ball])(upper)
    final = sd.translate([0,0,d_ball/np.sqrt(2)/2-1])(final)
    final = sd.intersection()(final, upper)
    final = sd.scad_render(final, file_header=f'$fn={fn};')
    print(final)


