import math
import numpy as np

def dist(vec1, vec2):
    return math.sqrt(sum(coor ** 2 for coor in vec1 - vec2))

class Wall:
    def __init__(self, f, L, dim):
        """Creates a double wall.

            Args:
                f: The toughness of the wall.
                L: The distance from zero to the wall.
                dim: The direction of the wall, equal 0, 1, or 2,
                    corresponding to x, y and z axes. 
        """
        self.f = f
        self.L = L
        self.dim = dim
        assert dim in [0, 1, 2]

    def calc_force(self, atom_nr, system):
        """Computes forces from the wall acting on atom."""
        atom = system.atoms[atom_nr]
        r = abs(atom.coors[self.dim])
        if r <= self.L:
            return np.zeros(3)
        else:
            force = np.zeros(3)
            force[self.dim] = -np.sign(atom.coors[self.dim]) * self.f \
                * (r - self.L)
            return force

    def calc_U_atom(self, atom):
        """Computes potential energy of the atom from the wall."""
        r = abs(atom.coors[self.dim])
        if r <= self.L:
            return 0
        else: # r2 > self.L2
            return 0.5 * self.f * (r - self.L) ** 2

    def calc_U(self, system):
        """Computes potential energy of a system due to the wall."""
        totalU = 0
        for atom in system.atoms:
            totalU += self.calc_U_atom(atom)
        return totalU

class VdW:
    def __init__(self, E=1.0, R=1.0):
        self.E = E
        self.R = R

    def calc_U_atom_pair(self, atom1, atom2):
        """Calculates the VdW potential between two atoms."""
        p = (self.R / dist(atom1.coors, atom2.coors)) ** 6
        return self.E * p * (p  - 2)
 #E((R/r)^12-2(R/r)^6)
    def calc_U(self, system):
        """Computes potential energy of a system due to VdW interactions."""
        totalU = 0
        for i in range(len(system.atoms)):
            for j in range(i + 1, len(system.atoms)):
                totalU += self.calc_U_atom_pair(system.atoms[i],
                                                system.atoms[j])
        return totalU

    def calc_force_atom_pair(self, atom1, atom2):
        """Calculates the VdW force acting on atom1 from atom2."""
        d = dist(atom1.coors, atom2.coors)
        inv = self.R / d
        p = inv ** 6
        return self.E * 12 * (p - 1) * p / (d ** 2) * \
            (atom1.coors - atom2.coors)

    def calc_force(self, atom_nr, system):
        """Computes total VdW force acting on an atom with nr atom_nr."""
        force = np.zeros(3)
        system.atoms
        atom = system.atoms[atom_nr]
        for i, atom2 in enumerate(system.atoms):
            if (i != atom_nr):
                force += self.calc_force_atom_pair(atom, atom2)
        return force

