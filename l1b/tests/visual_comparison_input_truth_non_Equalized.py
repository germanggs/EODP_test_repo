from pathlib import Path

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

# ============================================================
# 1. DIRECTORIES
# ============================================================

truth_dir = Path(
    r"C:\EODP_test_repo\EODP_test_repo\EODP_TER_2021\EODP-TS-L1B\input"
)

equalized_dir = Path(
    r"C:\EODP_test_repo\EODP_test_repo\EODP_TER_2021\EODP-TS-L1B\Output_German_2"
)

non_equalized_dir = Path(
    r"C:\EODP_test_repo\EODP_test_repo\EODP_TER_2021\EODP-TS-L1B\non_equalized"
)

# Folder where plots will be saved
save_dir = equalized_dir / "comparison_line_plots"
save_dir.mkdir(parents=True, exist_ok=True)

# ============================================================
# 2. FILE MAPPING
# ============================================================

# Input folder uses ism_toa_VNIR-X.nc
# Other folders use l1b_toa_VNIR-X.nc

files = {
    "VNIR-0": {
        "truth": "ism_toa_VNIR-0.nc",
        "equalized": "l1b_toa_VNIR-0.nc",
        "non_equalized": "l1b_toa_VNIR-0.nc",
    },
    "VNIR-1": {
        "truth": "ism_toa_VNIR-1.nc",
        "equalized": "l1b_toa_VNIR-1.nc",
        "non_equalized": "l1b_toa_VNIR-1.nc",
    },
    "VNIR-2": {
        "truth": "ism_toa_VNIR-2.nc",
        "equalized": "l1b_toa_VNIR-2.nc",
        "non_equalized": "l1b_toa_VNIR-2.nc",
    },
    "VNIR-3": {
        "truth": "ism_toa_VNIR-3.nc",
        "equalized": "l1b_toa_VNIR-3.nc",
        "non_equalized": "l1b_toa_VNIR-3.nc",
    },
}

# ============================================================
# 3. OPTIONS
# ============================================================

# If the NetCDF file has exactly one 2D variable, it will be used automatically.
# If not, set the name explicitly here, e.g. VARIABLE_NAME = "toa"
VARIABLE_NAME = None

# How to reduce 2D data to a 1D profile for plotting:
# "mean_rows"  -> mean across rows, value vs column index
# "mean_cols"  -> mean across columns, value vs row index
# "row"        -> use one specific row
# "col"        -> use one specific column
PROFILE_MODE = "mean_rows"

# Used only if PROFILE_MODE == "row" or "col"
PROFILE_INDEX = 0

# ============================================================
# 4. READ NETCDF
# ============================================================

def read_netcdf_2d(filepath):
    """
    Read a 2D array from a NetCDF file.
    """

    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    with xr.open_dataset(filepath) as ds:

        if VARIABLE_NAME is not None:
            if VARIABLE_NAME not in ds.data_vars:
                raise KeyError(
                    f"Variable '{VARIABLE_NAME}' not found in {filepath.name}. "
                    f"Available variables: {list(ds.data_vars)}"
                )
            variable = VARIABLE_NAME

        else:
            candidates = []

            for var in ds.data_vars:
                arr = np.squeeze(ds[var].values)
                if arr.ndim == 2:
                    candidates.append(var)

            if len(candidates) == 0:
                raise ValueError(
                    f"No 2D variable found in {filepath.name}. "
                    f"Available variables: {list(ds.data_vars)}"
                )

            if len(candidates) > 1:
                raise ValueError(
                    f"Multiple 2D variables found in {filepath.name}: {candidates}. "
                    f"Set VARIABLE_NAME explicitly."
                )

            variable = candidates[0]

        data = np.asarray(np.squeeze(ds[variable].values), dtype=np.float64)

        if data.ndim != 2:
            raise ValueError(
                f"{filepath.name}: expected 2D data, got shape {data.shape}"
            )

        print(
            f"Loaded {filepath.name} | variable = {variable} | shape = {data.shape}"
        )

        return data

# ============================================================
# 5. BUILD 1D PROFILE
# ============================================================

def build_profile(data_2d, mode="mean_rows", profile_index=0):
    """
    Convert a 2D array to a 1D profile.
    """

    if mode == "mean_rows":
        # One value per column
        profile = np.nanmean(data_2d, axis=0)
        x = np.arange(profile.size)
        xlabel = "Index"
        return x, profile, xlabel

    elif mode == "mean_cols":
        # One value per row
        profile = np.nanmean(data_2d, axis=1)
        x = np.arange(profile.size)
        xlabel = "Index"
        return x, profile, xlabel

    elif mode == "row":
        if profile_index < 0 or profile_index >= data_2d.shape[0]:
            raise IndexError(
                f"PROFILE_INDEX={profile_index} out of bounds for rows "
                f"(0 to {data_2d.shape[0]-1})"
            )
        profile = data_2d[profile_index, :]
        x = np.arange(profile.size)
        xlabel = "Index"
        return x, profile, xlabel

    elif mode == "col":
        if profile_index < 0 or profile_index >= data_2d.shape[1]:
            raise IndexError(
                f"PROFILE_INDEX={profile_index} out of bounds for columns "
                f"(0 to {data_2d.shape[1]-1})"
            )
        profile = data_2d[:, profile_index]
        x = np.arange(profile.size)
        xlabel = "Index"
        return x, profile, xlabel

    else:
        raise ValueError(
            "PROFILE_MODE must be one of: "
            "'mean_rows', 'mean_cols', 'row', 'col'"
        )

# ============================================================
# 6. METRICS
# ============================================================

def profile_metrics(truth_profile, other_profile):
    valid = np.isfinite(truth_profile) & np.isfinite(other_profile)

    if not np.any(valid):
        return {
            "MAE": np.nan,
            "RMSE": np.nan,
            "Bias": np.nan,
        }

    error = other_profile[valid] - truth_profile[valid]

    return {
        "MAE": np.mean(np.abs(error)),
        "RMSE": np.sqrt(np.mean(error**2)),
        "Bias": np.mean(error),
    }

# ============================================================
# 7. MAIN LOOP - GENERATE 4 LINE PLOTS
# ============================================================

for band, names in files.items():

    print("\n" + "=" * 70)
    print(f"COMPARING {band}")
    print("=" * 70)

    truth_2d = read_netcdf_2d(truth_dir / names["truth"])
    equalized_2d = read_netcdf_2d(equalized_dir / names["equalized"])
    non_equalized_2d = read_netcdf_2d(non_equalized_dir / names["non_equalized"])

    if not (
        truth_2d.shape == equalized_2d.shape == non_equalized_2d.shape
    ):
        raise ValueError(
            f"Shape mismatch in {band}:\n"
            f"Truth: {truth_2d.shape}\n"
            f"Equalized: {equalized_2d.shape}\n"
            f"Non-equalized: {non_equalized_2d.shape}"
        )

    x_truth, truth_profile, xlabel = build_profile(
        truth_2d,
        mode=PROFILE_MODE,
        profile_index=PROFILE_INDEX
    )

    x_eq, equalized_profile, _ = build_profile(
        equalized_2d,
        mode=PROFILE_MODE,
        profile_index=PROFILE_INDEX
    )

    x_non, non_equalized_profile, _ = build_profile(
        non_equalized_2d,
        mode=PROFILE_MODE,
        profile_index=PROFILE_INDEX
    )

    if not (len(x_truth) == len(x_eq) == len(x_non)):
        raise ValueError(f"Profile length mismatch in {band}")

    metrics_eq = profile_metrics(truth_profile, equalized_profile)
    metrics_non = profile_metrics(truth_profile, non_equalized_profile)

    print("Equalized vs Truth:", metrics_eq)
    print("Non-equalized vs Truth:", metrics_non)

    # --------------------------------------------------------
    # PLOT
    # --------------------------------------------------------

    plt.figure(figsize=(12, 7))

    plt.plot(
        x_truth,
        truth_profile,
        color="blue",
        linewidth=2,
        label="True"
    )

    plt.plot(
        x_non,
        non_equalized_profile,
        color="red",
        linewidth=2,
        label="Non-equalized"
    )

    plt.plot(
        x_eq,
        equalized_profile,
        color="black",
        linewidth=2,
        label="Equalized"
    )

    plt.title(
        f"{band}: True vs Non-equalized vs Equalized",
        fontsize=18
    )

    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel("Value", fontsize=14)

    plt.legend(fontsize=13)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = save_dir / f"{band}_line_comparison.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")

    print(f"Saved plot: {output_path}")

    plt.show()
    plt.close()

print("\nDone. 4 line plots created.")