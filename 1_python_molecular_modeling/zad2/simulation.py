import lattice, metropolis, argparse, os, random
import numpy as np
import matplotlib.pyplot as plt

def is_polar(c):
    assert c == 'P' or c == 'H'
    if c == 'P':
        return True
    else:
        return False

class CvCalculator:
    def __init__(self, T):
        self.T = T
        # sum of Boltzmann factors pi = exp(-Ei/kT), where we take k = 1
        self.Z = 0
        # sum of Boltzmann factors pi multiplied by energies Ei
        self.sumpiEi = 0
        # sum of Boltzmann factors pi multiplied by square Ei
        self.sumpiEi2 = 0
        
    def add_energy(self, Ei):
        pi = np.exp(-Ei / self.T)     
        self.Z += pi
        piEi = pi * Ei
        self.sumpiEi += piEi
        self.sumpiEi2 += piEi * Ei
        
    def calc(self):
        aveEi = self.sumpiEi / self.Z
        aveEi2 = self.sumpiEi2 / self.Z
        return (aveEi2 - aveEi ** 2) / (self.T ** 2) 
        
def printCvs(Cv_calcs, base_filename):
    Ts = [Cv_calc.T for Cv_calc in Cv_calcs]
    Cvs = [Cv_calc.calc() for Cv_calc in Cv_calcs]
    plt.clf()
    plt.plot(Ts, Cvs, 'r')
    plt.title("Plot of Cv(T)")
    energy_graph_filename =  base_filename + "_Cv_graph.png"
    plt.savefig(energy_graph_filename) 

class Simulation:
    def __init__(self, T0_min=0.40, T0_max=1.5, T_end_min=0.15, 
                 dT=0.05, num_steps_per_T=2000, num_steps_rep_change=1, max_num_pdb_files=25):
        self.T0_min = T0_min
        self.T0_max = T0_max
        self.dT = dT
        # number of replicas
        self.num_replicas = int(round((T0_max - T0_min) / dT)) + 1
        self.num_pdb_files = min(max_num_pdb_files, self.num_replicas)        
        # Number of temperatures considered for each replica.
        self.num_T = int(round((T0_min - T_end_min) / dT)) + 1
        # Number of Metropolis steps for each temperature.
        self.num_steps_per_T = num_steps_per_T
        # Per how many steps change replicas.
        self.num_steps_rep_change = num_steps_rep_change

    def get_T_array(self, T_min):
        return [T_min + i * self.dT for i in range(self.num_replicas)]

    def get_replicas(self, residues):
        replicas = []
        for i in range(self.num_replicas):
            coors_list = [(j, 0, 0) for j in range(len(residues))]
            lat = lattice.Lattice(residues, coors_list, i)
            replicas.append(lat)

        return replicas

    def run(self, protein_str, base_dir):
        print "Running for protein ", protein_str
        rg = metropolis.RotationGenerator()
        metr = metropolis.Metropolis()
        residues = [lattice.Residue(is_polar(c), i) \
                    for i, c in enumerate(protein_str, 1)]
        base_filename = base_dir + protein_str
        replicas = self.get_replicas(residues)
        pdb_files = [open(base_filename + '_replica_{:02d}'.format(i + 1) + ".pdb", 'w') 
                     for i in range(self.num_pdb_files)]
        for i in xrange(self.num_pdb_files):
            pdb_files[i].write(replicas[i].pdb_str())
        num_Cvs = self.num_replicas - self.num_T + 1
        Cv_calcs = [CvCalculator(self.T0_min + i * self.dT) \
                    for i in range(num_Cvs)]
        # For each temperature range.
        for i in range(self.num_T):
            T_arr = self.get_T_array(self.T0_min - i * self.dT)
            print "Temp range", i, "temperatures from", T_arr[0], "to", T_arr[-1] 
            # Running a Metropolis step for each replica.
            for step in xrange(self.num_steps_per_T):
                for j, lat in enumerate(replicas):
                    metr.make_step(lat, T_arr[j], rg)
                    if lat.nr < self.num_pdb_files:
                        pdb_files[lat.nr].write(lat.pdb_str()) 
                    Cv_ind = j - i
                    if Cv_ind >= 0 and Cv_ind < num_Cvs:
                        Cv_calcs[Cv_ind].add_energy(lat.get_energy())
                if step % self.num_steps_rep_change == 0:
                    i1 = random.choice(range(self.num_replicas - 1 ))
                    i2 = i1 + 1
                    diff = (replicas[i1].get_energy() - replicas[i2].get_energy()) \
                        * (1 / T_arr[i1] - 1 / T_arr[i2])
                    if random.uniform(0, 1) < np.exp(diff):
                        replicas[i1], replicas[i2] = replicas[i2], replicas[i1]     
        for f in pdb_files:
            f.close()
        printCvs(Cv_calcs, base_filename)
        
        with open(base_filename + "_final_T_Replicas.txt", 'w') as f:
            print >> f, "T\tReplica\n", 
            for i in range(self.num_replicas):
                print >> f, str(T_arr[i]) + "\t" + str(replicas[i].nr + 1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseDir', required=True)
    parser.add_argument('--sequence', required=True)
    args = parser.parse_args()
    base_dir = os.path.normpath(args.baseDir) + "/"
    sim = Simulation()
    sim.run(protein_str=args.sequence,
            base_dir=base_dir)
