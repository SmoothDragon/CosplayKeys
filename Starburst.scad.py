#!/usr/bin/env python

'''Inspired by conversation with Jason Devinney.
Print in vase mode with zero bottom layers.
'''

import solid2 as sd



if __name__ == '__main__':
    fn = 256
    R = 25
    r = 6

    final = sd.circle(R)
    arm = sd.hull()(sd.circle(r).translate([2*r,0]), sd.circle(r).translate([R,0]))
    final -= sd.union()(*[sd.rotate(60*i)(arm) for i in range(6)])
    final = sd.minkowski()(final, sd.circle(r/2))
    final = sd.linear_extrude(10)(final)
    final = sd.scad_render(final, file_header=f'$fn={fn};')
    print(final)


