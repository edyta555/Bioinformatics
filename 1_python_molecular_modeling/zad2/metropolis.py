import numpy as np
import random
import lattice                  

class RotationGenerator:
    def __init__(self):
        rot0_2d = np.eye(2, dtype=int)
        rot90_2d = np.array([[0, -1], [1, 0]])
        rot180_2d = rot90_2d.dot(rot90_2d)
        rot270_2d = rot180_2d.dot(rot90_2d)
        rots_2d = [rot0_2d, rot90_2d, rot180_2d, rot270_2d]
        self.rots_3d = []
        for i in range(3):
            # generates 4 rotation matrices around axis i
            rots_i = []
            # the indices of the plane in which rotation occurs
            plane_inds = [j for j in range(3) if j != i]
            for rot_2d in rots_2d:
                rot_3d = np.eye(3, dtype=int)
                for k1 in range(2):
                    for k2 in range(2):
                        rot_3d[plane_inds[k1], plane_inds[k2]] = rot_2d[k1][k2]
                rots_i.append(rot_3d)
            self.rots_3d.append(rots_i)

    def generate_random(self):
        inds = range(3)
        random.shuffle(inds)
        rot_inds = [0, 0, 0]
        # we do not want an identity matrix
        while rot_inds == [0, 0, 0]:
            rot_inds = [random.choice(range(4)) for _ in range(3)]
        
        total_rot = np.eye(3, dtype=int)
        for i in inds:
            total_rot = total_rot.dot(self.rots_3d[i][rot_inds[i]])
        return total_rot

class Metropolis:
    def transform_coors(self, coors_list, mat, last_still):
        """Transforms coors_list by matrix mat starting from position last_still.
        
        Returns: A list of new coordinates or None if there is a collision.
        """
        origin = np.array(coors_list[last_still])
        still_coors = set(coors_list[i] for i in range(last_still + 1))
        new_coors_list = coors_list[:last_still + 1]
        for i in range(last_still + 1, len(coors_list)):
            coors_old = np.array(coors_list[i])
            coors = origin + mat.dot((coors_old - origin))
            if tuple(coors) in still_coors:
                return None
            new_coors_list.append(tuple(coors)) 
        return new_coors_list

    def random_transform_coors(self, lat, rot_gen):
        """Transforms lattice by a random matrix starting from random position.
        
        Returns: A list of new coordinates or None if there is a collision.
        """
        mat = rot_gen.generate_random()
        num_coors = len(lat.coors_list)
        last_still = random.choice(range(num_coors - 1))
        return self.transform_coors(lat.coors_list, mat, last_still)

    def make_step(self, lat, T, rot_gen):
        """Performs a Metropolis step on the lattice lat."""
        new_coors_list = self.random_transform_coors(lat, rot_gen)
        if new_coors_list is not None:
            new_lat = lattice.Lattice(lat.residues, new_coors_list)
            curr_energy = lat.get_energy()
            new_energy = new_lat.get_energy()
            if new_energy <= curr_energy:
                lat.set_coors_list(new_coors_list)
            else:
                r = np.exp(-(new_energy - curr_energy) / T)
                if random.uniform(0, 1) < r:
                    lat.set_coors_list(new_coors_list)


