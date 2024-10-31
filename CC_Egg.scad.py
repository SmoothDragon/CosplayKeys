#!/usr/bin/env python

'''Twisting egg
'''

import solid2 as sd
import svgSCAD as d2

if __name__ == '__main__':
    fn = 256

    r = 30

    final = d2.egg(r)
    final = sd.linear_extrude(height=10)(final)

    final = sd.scad_render(final, file_header=f'$fn={fn};')
    print(final)


