from pathlib import Path
import numpy as np
from netCDF4 import Dataset

root = Path(__file__).resolve().parents[1]
base = root / "EODP_TER_2021" / "EODP-TS-L1C"

reference_dir = base / "output"
actual_dir = base / "Output_L1C_updated_20261022"

tolerance = 1e-5

reference_files = sorted(reference_dir.glob("*.nc"))

if len(reference_files) != 4:
    raise ValueError("Expected 4 L1C reference files")

failed = 0

for reference_path in reference_files:
    actual_path = actual_dir / reference_path.name

    if not actual_path.exists():
        print("MISSING:", reference_path.name)
        failed += 1
        continue



    with Dataset(reference_path) as ref, Dataset(actual_path) as actual:
        ref_lat = np.asarray(ref.variables["lat"][:])
        ref_lon = np.asarray(ref.variables["lon"][:])

        actual_lat = np.asarray(actual.variables["lat"][:])
        actual_lon = np.asarray(actual.variables["lon"][:])

        # Sort both datasets by latitude, then longitude
        ref_order = np.lexsort((ref_lon, ref_lat))
        actual_order = np.lexsort((actual_lon, actual_lat))

        coordinates_ok = (
            np.array_equal(ref_lat[ref_order], actual_lat[actual_order])
            and np.array_equal(ref_lon[ref_order], actual_lon[actual_order])
        )

        # Apply the same ordering to the radiances
        expected = np.asarray(
            ref.variables["toa"][:], dtype=float
        )[ref_order]

        obtained = np.asarray(
            actual.variables["toa"][:], dtype=float
        )[actual_order]

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

    passed = coordinates_ok and finite and relative_ok and zeros_ok
    label = "PASS" if passed else "FAIL"
    print(label, reference_path.name)

    if not passed:
        failed += 1

print("Files checked:", len(reference_files))
print("Failed:", failed)

raise SystemExit(1 if failed else 0)