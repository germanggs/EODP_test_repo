from pathlib import Path
import numpy as np
from netCDF4 import Dataset

root = Path(__file__).resolve().parents[1]
base = root / "EODP_TER_2021" / "EODP-TS-L1B"

reference_dir = base / "output"
actual_dir = base / "Output_L1B_python311"

tolerance = 1e-5

reference_files = sorted(reference_dir.glob("*.nc"))

if len(reference_files) != 8:
    raise ValueError("Expected 8 L1B reference files")

failed = 0
overall_max_error_percent = 0.0


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

    max_error_percent = np.inf

    if finite:
        max_error_percent = 0.0

        if np.any(nonzero):
            max_error_percent = 100 * np.max(
                difference[nonzero] / np.abs(expected[nonzero])
            )

    overall_max_error_percent = max(
        overall_max_error_percent, max_error_percent
    )

    print(
        label,
        reference_path.name,
        f"| Maximum relative error: {max_error_percent:.8e}%"
    )

    if not passed:
        failed += 1

print("Files checked:", len(reference_files))
print("Failed:", failed)
print(
    f"Overall maximum relative error: "
    f"{overall_max_error_percent:.8e}%"
)
print("Required: relative error < 0.001%")

raise SystemExit(1 if failed else 0)