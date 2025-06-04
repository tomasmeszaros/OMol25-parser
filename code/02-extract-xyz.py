from fairchem.core.datasets.ase_datasets import AseDBDataset
import os
from ase.data import chemical_symbols
allowed_atomic_numbers = {
    1,    # H
    6, 7, 8, 15, 16,             # C, N, O, P, S
    9, 17, 35, 53,               # F, Cl, Br, I
    3, 11, 19,                   # Li, Na, K
    12, 20                       # Mg, Ca
}

valid_molecules = []
# Inicializace datasetu v train_4M
config = {"src": "../data/train_4M"}
dataset = AseDBDataset(config=config)
directory = os.makedirs("../data/xyz", exist_ok=True)
for i in range(5):
    try:
        atoms = dataset.get_atoms(i)
        atomic_numbers = atoms.get_atomic_numbers()
        charge = atoms.info.get("charge", 0)
        if all(Z in allowed_atomic_numbers for Z in atomic_numbers):
            valid_molecules.append(i)
            f = open(f"../data/xyz/molecule{i}.xyz", "w")
            f.write(f"{len(atoms)}\n")
            f.write(f"charge={charge}\n")
            for j, pos in enumerate(atoms.get_positions()):
                Z = atomic_numbers[j]
                symbol = chemical_symbols[Z]
                x, y, z = pos
                f.write(f"{symbol} {x} {y} {z}\n")
                
    except Exception:
        continue
print(len(valid_molecules))

