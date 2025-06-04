from collections import defaultdict
from fairchem.core.datasets.ase_datasets import AseDBDataset
from tqdm import tqdm

allowed_atomic_numbers = {
    1,    # H
    6, 7, 8, 15, 16,             # C, N, O, P, S
    9, 17, 35, 53,               # F, Cl, Br, I
    3, 11, 19,                   # Li, Na, K
    12, 20                       # Mg, Ca
}

config = {"src": "../data/train_4M"}
dataset = AseDBDataset(config=config)

subset_stats = defaultdict(lambda: {"total": 0, "valid": 0, "atom_count_sum": 0})

for i in tqdm(range(len(dataset)), desc="Analyzujeme molekuly"):
    try:
        atoms = dataset.get_atoms(i)
        data_id = atoms.info.get("data_id", "UNKNOWN")
        atomic_numbers = atoms.get_atomic_numbers()
        is_valid = all(Z in allowed_atomic_numbers for Z in atomic_numbers)

        subset_stats[data_id]["total"] += 1
        if is_valid:
            subset_stats[data_id]["valid"] += 1
            subset_stats[data_id]["atom_count_sum"] += len(atomic_numbers)
    except Exception:
        continue

print(f"{'Subset':<30} {'Platné molekuly':>15} {'Průměrná velikost':>20} {'Celkem':>10}")
print("=" * 80)

for subset, stats in sorted(subset_stats.items()):
    valid = stats["valid"]
    total = stats["total"]
    avg_size = stats["atom_count_sum"] / valid if valid > 0 else 0
    print(f"{subset:<30} {valid:>15} {avg_size:>20.2f} {total:>10}")

