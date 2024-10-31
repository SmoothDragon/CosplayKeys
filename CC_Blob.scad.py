#!/usr/bin/env python

'''Twisting egg
'''

import solid2 as sd
import svgSCAD as d2

if __name__ == '__main__':
    fn = 128

    D = 200


    r = 30

    base = sd.square(D, center=True)
    final = sd.square(D, center=True)
    final -= sd.circle(r=25)
    final -= sd.translate([-10,-10])(sd.circle(25))
    final -= sd.translate([15,15])(sd.circle(10))
    final -= sd.translate([25,-15])(sd.circle(20))
    final -= sd.translate([-25,-5])(sd.circle(15))
    final = sd.minkowski()(final, sd.circle(5))
    final = base-final

    final = sd.linear_extrude(height=10)(final)

    final = sd.scad_render(final, file_header=f'$fn={fn};')
    print(final)


