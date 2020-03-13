class Residue:
    def __init__(self, is_polar, nr):
        self.polar = is_polar
        self.nr = nr

    def get_pdb_atom_name(self):
        if self.polar:
            return 'P'
        else:
            return 'C' # H does not form a chain in VMD

    def pdb_line(self, coors):
        line = "ATOM  " + str(self.nr).rjust(5) + " "\
            + self.get_pdb_atom_name().center(4)\
            + " GLY A   1    "
        for coor in coors:
            line += str(round(coor, 3)).rjust(8)
        line += "  0.00  0.00\n"
        return line

def iter_neighbours(coors):
    """Yields all neighbours of coors."""
    for s in [-1, 1]:
        for i in range(3): # considering different coordinates to change.
            neigh_coors = list(coors)
            neigh_coors[i] += s
            yield tuple(neigh_coors)

class Lattice:
    def __init__(self, residues, coors_list, nr=0):
        self.residues = residues
        self.set_coors_list(coors_list)
        self.nr = nr

    def set_coors_list(self, coors_list):
        self.coors_list = coors_list
        self.coors_res = {
            tuple(coors_list[i]): self.residues[i] for i in range(len(coors_list))
        }

    def get_num_h_contacts(self):
        """Returns the number of hydrophobic contacts in the protein."""
        num_h_contacts = 0
        for coors, res in self.coors_res.iteritems():
            if not res.polar:
                for neigh_coors in iter_neighbours(coors):
                    if neigh_coors in self.coors_res:
                        neigh_res = self.coors_res[neigh_coors]
                        if not neigh_res.polar and neigh_res.nr > res.nr + 1:
                            num_h_contacts += 1
        return num_h_contacts

    def get_energy(self):
        return - float(self.get_num_h_contacts())

    def pdb_str(self):
        s = "MODEL\n"
        for i, res in enumerate(self.residues):
            s += res.pdb_line(self.coors_list[i])
        s += "TER\nENDMDL\n"
        return s

    def pdb_close(self):
        self.pdb_file.close()  
