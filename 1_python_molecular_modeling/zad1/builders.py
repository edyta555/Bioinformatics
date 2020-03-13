import simulation, forcefields, atoms, integrators
import numpy as np
import argparse
import os

# This module contains functions building various simulations.

def create_collision_wall(integrator, f=20, L=1):
    """Creates a simulation of a collision with a wall."""
    a = atoms.Neon([0, 0, 0], [1, 0, 0])
    atom_list = [a]
    s = atoms.System(atom_list)
    fWall = forcefields.Wall(f, L, 0)
    return simulation.Simulation(s, [fWall], integrator)

def create_collision_atoms(integrator, atom1, atom2):
    """Creates a simulation of a collision between two atoms."""
    s = atoms.System([atom1, atom2])
    return simulation.Simulation(s, [forcefields.VdW()], integrator)

def create_collision_crystal(integrator, R0=1, n=8, d=1, v=1):
    """Creates a simulation of a collision of an atom and a crystal.

    Some args:
        n: The crystal has n * n * n atoms.
        R0: Distance of two atoms corresponding to the minimum of the of the
            VdW potential between them.
        d: Distance from the crystal of the bombarding atom.
        v: Velocity in direction of the crystal of the bombarding atom.
    """
    middle = (R0 / 2.0) * (n - 1)
    bombarding_atom = atoms.Gold([-d, middle, middle], [v, 0, 0])
    atom_list = [bombarding_atom]
    lists =  [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    arrays = [np.array(l) for l in lists]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                coors = R0 * (i * arrays[0] + j * arrays[1] \
                              + k * arrays[2])
                atom_list.append(atoms.Gold(coors, [0, 0, 0]))   
    s = atoms.System(atom_list)
    VdW = forcefields.VdW(R=R0)
    return simulation.Simulation(s, [VdW], integrator)


def create_gas_box(integrator, n=10, b=1, L=3, f=20, seed=0):
    """Creates a simulation of a box with neon gas.

    Some args:
        n: The number of particles of gas.
        f: The stiffness of the walls of the box.
        L: The half of width of the box.
        b: The coordinates of velocities have uniform distribution on [-b, b].
        seed: The seed of the random number generator.
    """

    FF_list = [forcefields.Wall(f, L, i) for i in range(3)]
    FF_list.append(forcefields.VdW())
    atom_list = []
    dim = 3
    np.random.seed(seed)
    for i in range(n):
        atom_list.append(atoms.Neon(np.random.uniform(-L,L,dim),
                                    np.random.uniform(-b,b,dim)))
    return simulation.Simulation(atoms.System(atom_list),
                                 FF_list, integrator)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseDir', required=True)
    args = parser.parse_args()
    base_dir = os.path.normpath(args.baseDir) + "/"
    print "Collision with wall, Euler scheme."            
    sim = create_collision_wall(integrators.Euler())
    sim.run_n_steps(base_filename=base_dir + "wall_euler", n=3000, dt=0.01)

    print "Collision with a wall, Verlet scheme."    
    sim = create_collision_wall(integrators.Verlet())
    sim.run_n_steps(base_filename=base_dir + "wall_verlet", n=3000, dt=0.01)

    print "Head on collision of atoms."
    sim = create_collision_atoms(
        integrators.Verlet(), atoms.Neon([0, 0, 0], [1, 0, 0]),
        atoms.Neon([2, 0, 0], [-1, 0, 0]))
    sim.run_n_steps(base_filename=base_dir + "collision_atoms_head_on", 
                    n=2000, dt=0.001)

    print "Oblique collision of atoms."
    sim = create_collision_atoms(
        integrators.Verlet(), atoms.Neon([0, 0, 0], [1, 0, 0]),
        atoms.Neon([2, 0.25, 0], [-1, 0, 0]))
    sim.run_n_steps(base_filename=base_dir + "collision_atoms_oblique", 
                    n=2000, dt=0.001)

    print "Collision of an atom and a crystal."
    sim = create_collision_crystal(integrators.Verlet(), R0=1, n=2, d=1, v=1)
    sim.run_n_steps(base_filename=base_dir + "collision_crystal", n=6000, 
                    dt=0.002)
    
    print "gas in a box."
    sim = create_gas_box(integrators.Verlet(), n=10, b=1, L=2, f=20)
    sim.run_n_steps(base_filename=base_dir + "gas_box", 
                    n=20000, dt=0.001)
