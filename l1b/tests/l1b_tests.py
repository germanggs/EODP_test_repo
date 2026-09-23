
from pathlib import Path
import numpy as np
import xarray as xr
import difflib

# Directories
dir1 = Path(r"C:\EODP_test_repo\EODP_test_repo\EODP_TER_2021\EODP-TS-L1B\Output_German_2")
dir2 = Path(r"C:\EODP_test_repo\EODP_test_repo\EODP_TER_2021\EODP-TS-L1B\output")

# Numerical comparison settings
RTOL = 0.0
ATOL = 0.0
EQUAL_NAN = True


def compare_netcdf(file1, file2):
    """Compare two NetCDF files, variable by variable and element by element."""
    identical = True

    with xr.open_dataset(file1, decode_cf=False) as ds1, \
         xr.open_dataset(file2, decode_cf=False) as ds2:

        # Compare global attributes
        if ds1.attrs != ds2.attrs:
            print("  Different global attributes")
            identical = False

        # Compare dimensions
        if dict(ds1.sizes) != dict(ds2.sizes):
            print("  Different dimensions:")
            print("    Folder 1:", dict(ds1.sizes))
            print("    Folder 2:", dict(ds2.sizes))
            identical = False

        # Compare variable names
        vars1 = set(ds1.variables)
        vars2 = set(ds2.variables)

        for name in sorted(vars1 - vars2):
            print(f"  Variable only in folder 1: {name}")
            identical = False

        for name in sorted(vars2 - vars1):
            print(f"  Variable only in folder 2: {name}")
            identical = False

        # Compare common variables
        for name in sorted(vars1 & vars2):
            v1 = ds1[name]
            v2 = ds2[name]

            if v1.dims != v2.dims or v1.shape != v2.shape:
                print(f"  {name}: different dimensions or shape")
                print(f"    Folder 1: {v1.dims}, {v1.shape}")
                print(f"    Folder 2: {v2.dims}, {v2.shape}")
                identical = False
                continue

            if v1.attrs != v2.attrs:
                print(f"  {name}: different attributes")
                identical = False

            a = v1.values
            b = v2.values

            if a.dtype != b.dtype:
                print(f"  {name}: different data types: {a.dtype} vs {b.dtype}")
                identical = False

            if np.issubdtype(a.dtype, np.number) and \
               np.issubdtype(b.dtype, np.number):

                # Compare every numerical element
                matches = np.isclose(
                    a, b,
                    rtol=RTOL,
                    atol=ATOL,
                    equal_nan=EQUAL_NAN
                )
            else:
                matches = a == b

            if np.all(matches):
                continue

            identical = False
            differences = np.argwhere(~matches)

            print(f"  {name}: {len(differences)} different elements")

            # Show the first 10 differences
            for index in differences[:10]:
                idx = tuple(index)
                print(f"    Index {idx}: {a[idx]} vs {b[idx]}")

            # Maximum numerical difference
            if np.issubdtype(a.dtype, np.number) and \
               np.issubdtype(b.dtype, np.number):

                with np.errstate(invalid="ignore", over="ignore"):
                    diff = np.abs(a.astype(float) - b.astype(float))
                    finite = diff[np.isfinite(diff)]

                if finite.size:
                    print(f"    Maximum absolute difference: {finite.max():.12g}")

    return identical


def compare_text(file1, file2):
    """Compare text files line by line."""
    lines1 = file1.read_text(
        encoding="utf-8", errors="replace"
    ).splitlines()

    lines2 = file2.read_text(
        encoding="utf-8", errors="replace"
    ).splitlines()

    if lines1 == lines2:
        return True

    differences = difflib.unified_diff(
        lines1, lines2,
        fromfile=str(file1),
        tofile=str(file2),
        lineterm=""
    )

    for line in differences:
        print(line)

    return False


# Compare all files
files1 = {p.name: p for p in dir1.iterdir() if p.is_file()}
files2 = {p.name: p for p in dir2.iterdir() if p.is_file()}

all_names = sorted(set(files1) | set(files2))

identical_files = []
different_files = []
missing_files = []

for name in all_names:
    print(f"\n{'=' * 60}")
    print(f"Comparing: {name}")

    if name not in files1:
        print("  MISSING from folder 1")
        missing_files.append(name)
        continue

    if name not in files2:
        print("  MISSING from folder 2")
        missing_files.append(name)
        continue

    file1 = files1[name]
    file2 = files2[name]

    try:
        if name.lower().endswith(".nc"):
            identical = compare_netcdf(file1, file2)

        elif name.lower().endswith((".log", ".txt")):
            identical = compare_text(file1, file2)

        else:
            # Byte-by-byte comparison for other file types
            identical = file1.read_bytes() == file2.read_bytes()

        if identical:
            print("  IDENTICAL")
            identical_files.append(name)
        else:
            print("  DIFFERENT")
            different_files.append(name)

    except Exception as e:
        print(f"  ERROR: {e}")
        different_files.append(name)


# Final summary
print(f"\n{'=' * 60}")
print("FINAL SUMMARY")
print(f"{'=' * 60}")
print(f"Identical files: {len(identical_files)}")
print(f"Different files: {len(different_files)}")
print(f"Missing files:   {len(missing_files)}")

if different_files:
    print("\nFiles with differences:")
    for name in different_files:
        print(f"  - {name}")

if missing_files:
    print("\nMissing files:")
    for name in missing_files:
        print(f"  - {name}")