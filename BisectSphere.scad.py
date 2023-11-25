#!/usr/bin/env python

'''Salt pig combined with Super Mario Brothers pipe
'''

import solid as sd
import numpy as np




if __name__ == '__main__':
    fn = 32
    d_ball = 100
    angle = 50

    final = sd.sphere(d=d_ball)
    cutter = sd.cube(d_ball, center=True)
    cutter = sd.translate([0,0,(np.sqrt(2)/4+.5)*d_ball])(cutter)
    cutter = sd.union()(*[sd.rotate([180*i/fn,0,0])(cutter) for i in range(fn)])

    cutter = sd.square(d_ball, center=True)
    cutter = sd.rotate(-45)(cutter)
    cutter = sd.intersection()(cutter,
            sd.translate([d_ball,0])(sd.square(2*d_ball, center=True)))
    cutter = sd.rotate_extrude(360)(cutter)
    cutter = sd.translate([0,0,d_ball*2**-.5])(cutter)
    cutter = sd.union()(*[sd.rotate([180*i/fn,0,0])(cutter) for i in range(fn+1)])

    final -= cutter
    final = sd.scad_render(final, file_header=f'$fn={fn};')
    print(final)


