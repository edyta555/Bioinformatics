#This module defines integrators of the form:
#class Integrator:
#def move(self, coor, prev_coor, v, a, dt):
#"""Returns new coordinates and velocity.
#
#Args:
#    coor: Current coordinates.
#    prev_coor: Previous coordinates.
#    v: Current veocity.
#    a: Current acceleration.
#    dt: Timestep.
# All arguments but the last one are numpy arrays.
#"""

class Euler:
    def move(self, coor, prev_coor, v, a, dt):
        return coor + v * dt, v + a * dt

class Verlet:
    def move(self, coor, prev_coor, v, a, dt):
        new_coor = 2 * coor - prev_coor + a * (dt ** 2)
        new_v = (new_coor - prev_coor)/(2 * dt) 
        return new_coor, new_v