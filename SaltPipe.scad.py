#!/usr/bin/env python

'''Salt pig combined with Super Mario Brothers pipe
'''

import solid as sd




if __name__ == '__main__':
    fn = 256
    d_lip = 100
    h_lip = 20
    h_wall = 5
    d_pipe = d_lip - 2*h_wall
    h_pipe = 20
    h_upper = h_lip+5
    d_hole = 80
    r_inner = 10
    angle = 50

    final = sd.cylinder(d=d_lip, h=h_lip)
    final += sd.cylinder(d=d_pipe, h=h_upper)
    final -= sd.cylinder(d=d_hole, h=3*h_pipe, center=True)
    bend = sd.circle(d=d_pipe) - sd.circle(d=d_hole)
    bend = sd.translate([d_pipe/2+r_inner,0])(bend)
    bend = sd.rotate_extrude(angle=angle)(bend)
    bend = sd.rotate([90,0,0])(bend)
    base = sd.cylinder(d=d_pipe, h=h_pipe)
    base -= sd.cylinder(d=d_hole, h=3*h_pipe, center=True)
    base += sd.cylinder(h=h_wall, d=d_pipe)
    base = sd.translate([d_pipe/2+r_inner,0,-h_pipe])(base)
    bend += base
    bend = sd.rotate([0,angle-180,0])(bend)
    bend = sd.translate([(d_pipe/2+r_inner),0,h_upper])(bend)
    final += bend

    final = sd.scad_render(final, file_header=f'$fn={fn};')
    print(final)


