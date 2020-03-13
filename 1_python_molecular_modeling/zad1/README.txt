W celu uruchomienia programu należy w bieżącym katalogu wpisać w terminalu:
python builders.py --baseDir path
gdzie path to pełna ścieżka do katalogu, w ktorym pojawią się wyniki symulacji.
python builders.py --baseDir /home/edyta/Desktop/PROGRAMY_MODELO/wyn


Dla różnych symulacji x, wyniki te mają postać plików:
x_energy_graph.png - wykres zależności energii całkowitej, potencjalnej i kinetycznej od czasu symulacji.
x_energy.txt - zależności różnych energii od czasu w postaci tekstowej.
x_trajectory.txt - zalezności położeń i prędkości kolejnych atomów od czasu.
x.pdb - plik pdb z 501 równoodległymi klatkami symulacji.

Rozważane x to:
wall_euler - zderzenie atomu neonu ze ścianą symulowane schematem Eulera.
wall_verlet - zderzenie atomu neonu ze ścianą symulowane schematem Verleta.
collision_atoms_head_on - zderzenie czołowe atomów neonu.
collision_atoms_onlique - zderzenie nieczołowe atomów neonu o początowych
                          położeniach (0, 0, 0) i (2, 0.25, 0) i prędkościach (1, 0, 0) i (-1, 0, 0).
collision_crystal - zderzenie atomu złota z sześciennym kryształem złota.
gass_box - pudełko z gazem (złożonym 10 atomów neonu)  o losowych początkowych
           położeniach i prędkościach.
