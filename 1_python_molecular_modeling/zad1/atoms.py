import numpy as np

class System:
    def __init__(self, atoms):
        self.atoms = atoms

    def pdb_str(self, t=0):
        s = "MODEL\n"
        for i, atom in enumerate(self.atoms, 1):
            s += atom.pdb_str(i)
        s += "TER\nENDMDL\n"
        return s

class Atom:
    def __init__(self, coors, v, mass, name, charge=0):
        self.mass = mass
        self.name = name
        self.charge = charge
        self.coors = np.array(coors)
        self.v = np.array(v)

    def pdb_str(self, nr):
        line = "ATOM  " + str(nr).rjust(5) + " "\
            + self.name.center(4)\
            + " GLY A   1    "
        for coor in self.coors:
            line += str(round(coor, 3)).rjust(8)
        line += "  0.00  0.00\n"
        return line

class Gold(Atom):
    def __init__(self, coors, v, charge=0):
        Atom.__init__(self, coors, v, 196.966, 'Au', charge)

class Neon(Atom):
    def __init__(self, coors, v, charge=0):
        Atom.__init__(self, coors, v, 20.180, 'Ne', charge)
    
    

