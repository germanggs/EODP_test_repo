from pathlib import Path
import numpy as np
from netCDF4 import Dataset

root = Path(__file__).resolve().parents[1]
base = root / "EODP_TER_2021" / "EODP-TS-ISM"

reference_dir = base / "output"
actual_dir = base / "Output_ISM_python311"
# 0.001% expressed as a fraction
tolerance = 1e-5

reference_files = sorted(reference_dir.glob("*.nc"))

if len(reference_files) != 56:
    raise ValueError("Expected 56 ISM reference files")

failed = 0

for reference_path in reference_files:
    actual_path = actual_dir / reference_path.name

    if not actual_path.exists():
        print("MISSING:", reference_path.name)
        failed += 1
        continue

    with Dataset(reference_path) as ref, Dataset(actual_path) as actual:
        variable = "mat" if "mat" in ref.variables else "toa"

        expected = np.asarray(ref.variables[variable][:], dtype=float)
        obtained = np.asarray(actual.variables[variable][:], dtype=float)

    if expected.shape != obtained.shape:
        print("SHAPE MISMATCH:", reference_path.name)
        failed += 1
        continue

    difference = np.abs(obtained - expected)
    nonzero = expected != 0

    finite = (
        np.all(np.isfinite(expected))
        and np.all(np.isfinite(obtained))
    )

    relative_ok = np.all(
        difference[nonzero] < tolerance * np.abs(expected[nonzero])
    )

    # Relative error is undefined at zero, so require an exact match there
    zeros_ok = np.all(obtained[~nonzero] == expected[~nonzero])

    passed = finite and relative_ok and zeros_ok
    label = "PASS" if passed else "FAIL"
    print(label, reference_path.name)

    if not passed:
        failed += 1

print("Files checked:", len(reference_files))
print("Failed:", failed)

raise SystemExit(1 if failed else 0)