import numpy as np
import matplotlib.pyplot as plt

def coor_list_str(coor_list):
    return ",".join(
        str(i) + ":(" + ",".join(["{0:.3f}".format(vi) for vi in v]) + ")"\
        for i, v in enumerate(coor_list, 1))

def output_energy_graph(base_filename, ts, E_tots, E_pots, E_kins):
    plt.clf() 
    plt.plot(ts, E_tots, 'r', label="E_tot")
    plt.plot(ts, E_pots, 'y', label="E_pot")
    plt.plot(ts, E_kins, 'g', label="E_kin")
    plt.title("Energies plot")
    plt.legend(loc='lower right')
    energy_graph_filename =  base_filename + "_energy_graph.png"
    plt.savefig(energy_graph_filename)

class Simulation(object):
    def __init__(self, system, FF_list, integrator):
        """Initializes simulation.

        Args:
            system: The simulated system.
            FF_list: A list of forcefieds.
            integrator: The integrator used.
        """
        self.system = system
        self.FF_list = FF_list
        self.integrator = integrator

    def run_n_steps(self, base_filename, dt=0.01, n=1000,
                    num_pdb_frames=1000, energy_out_per=1, traj_out_per=1):
        """Runs n step simulation. Outputs results to files.
        
        Some args:
        n: The number of simulation steps.
        num_pdb_frames: If n is divisible by it then it is the 
                number of outputted pdb frames - 1.
        """
        pdb_out_per = n / num_pdb_frames
        E_tots = []
        E_kins = []
        E_pots = []
        ts = [0]
        t = 0
        pdb_filename = base_filename +  ".pdb"
        energy_filename = base_filename + "_energy.txt"
        traj_filename = base_filename + "_trajectory.txt"
        with open(pdb_filename, 'w') as pdb_file,\
            open(energy_filename, 'w') as energy_file,\
            open(traj_filename, 'w') as traj_file:
            self.output_pdb(pdb_file)
            E_tot, E_kin, E_pot = self.output_energy(energy_file)
            E_tots.append(E_tot)
            E_kins.append(E_kin)
            E_pots.append(E_pot)
            self.output_traj(traj_file)
            self.prev_coors = [a.coors - a.v * dt for a in self.system.atoms]
            for i in range(n):
                self.run_single_step(dt)
                t += dt
                if i % pdb_out_per == 0:
                    self.output_pdb(pdb_file, t)
                if i % energy_out_per == 0:
                    E_tot, E_kin, E_pot = self.output_energy(energy_file, t)
                    E_tots.append(E_tot)
                    E_kins.append(E_kin)
                    E_pots.append(E_pot)
                    ts.append(t)
                if i % traj_out_per == 0:
                    self.output_traj(traj_file, t)

        output_energy_graph(base_filename, ts, E_tots, E_pots, E_kins)
        

    def run_single_step(self, dt):
        a_list = [] # list of accelerations
        for i, atom in enumerate(self.system.atoms):
            # Force acting on an atom.
            force = np.zeros(3)
            for FF in self.FF_list:
                force += FF.calc_force(i, self.system)
            # atom's acceleration
            a = force / float(atom.mass)
            a_list.append(a)
        
        for i, a in enumerate(a_list):
            atom = self.system.atoms[i]
            new_coors, new_v = self.integrator.move(
                atom.coors, self.prev_coors[i], atom.v, a, dt)
            self.prev_coors[i] = atom.coors
            atom.coors = new_coors
            atom.v = new_v

    def output_pdb(self, f, t=0):
        f.write(self.system.pdb_str(t))

    def output_traj(self, f, t=0):
        if t ==0:
            print >> f, "t\tcoordinates\tvelocities"
        print >> f, str(t) + '\t' \
            + coor_list_str([a.coors for a in self.system.atoms]) \
            + '\t' + coor_list_str([a.v for a in self.system.atoms])

    def calc_E_pot(self):
        E_pot = 0
        for FF in self.FF_list:
            E_pot += FF.calc_U(self.system)
        return E_pot

    def calc_E_kin(self):
        E_kin = 0
        for atom in self.system.atoms:
            E_kin += atom.mass * sum(vi ** 2 for vi in atom.v) / 2.0
        return E_kin

    def output_energy(self, f, t=0):
        if t == 0:
            print >> f, "t\tE_tot\tE_kin\tE_pot"
        E_kin = self.calc_E_kin()
        E_pot = self.calc_E_pot()
        E_tot = E_kin + E_pot
        print >> f, str(t) + "\t{0:.4f}\t{1:.4f}\t{2:.4f}".format(
            E_tot, E_kin, E_pot)
        return E_tot, E_kin, E_pot

        