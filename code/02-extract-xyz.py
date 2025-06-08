from fairchem.core.datasets.ase_datasets import AseDBDataset
import os
from ase.data import chemical_symbols
import tarfile

allowed_atomic_numbers = {
    1,    # H
    6, 7, 8, 15, 16,             # C, N, O, P, S
    9, 17, 35, 53,               # F, Cl, Br, I
    3, 11, 19,                   # Li, Na, K
    12, 20                       # Mg, Ca
}

valid_molecules = []
output_dir = "../data/xyz"
os.makedirs(output_dir, exist_ok=True)

config = {"src": "../data/train_4M"}
dataset = AseDBDataset(config=config)

batch_size = 1000
xyz_files = []
batch_index = 0

for i in range(len(dataset)):
    try:
        atoms = dataset.get_atoms(i)
        atomic_numbers = atoms.get_atomic_numbers()
        charge = atoms.info.get("charge", 0)

        if all(Z in allowed_atomic_numbers for Z in atomic_numbers):
            valid_molecules.append(i)
            filename = f"molecule{i}.xyz"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w") as f:
                f.write(f"{len(atoms)}\n")
                f.write(f"charge={charge}\n")
                for j, pos in enumerate(atoms.get_positions()):
                    Z = atomic_numbers[j]
                    symbol = chemical_symbols[Z]
                    x, y, z = pos
                    f.write(f"{symbol} {x} {y} {z}\n")

            xyz_files.append(filepath)

            if len(xyz_files) >= batch_size:
                tar_path = os.path.join(output_dir, f"xyz_batch_{batch_index}.tar")
                with tarfile.open(tar_path, "w") as tar:
                    for file_path in xyz_files:
                        tar.add(file_path, arcname=os.path.basename(file_path))
                        os.remove(file_path)
                xyz_files = []
                batch_index += 1

    except Exception:
        continue

if xyz_files:
    tar_path = os.path.join(output_dir, f"xyz_batch_{batch_index}.tar")
    with tarfile.open(tar_path, "w") as tar:
        for file_path in xyz_files:
            tar.add(file_path, arcname=os.path.basename(file_path))
            os.remove(file_path)
