
# MAIN FUNCTION TO CALL THE L1B MODULE

from l1b.src.l1b import l1b

# Directory - this is the common directory for the execution of the E2E, all modules
#auxdir = r"C:\EODP_test_repo\EODP_test_repo\auxiliary"
#indir = r"C:\EODP_test_repo\EODP_test_repo\EODP_TER_2021\EODP-TS-L1B\input"
#outdir = r"C:\EODP_test_repo\EODP_test_repo\EODP_TER_2021\EODP-TS-L1B\Output_L1B_python311"

auxdir = r"C:\EODP_test_repo\EODP_test_repo\auxiliary" #esto es para la ultima parte del report si no estamos en esa parte, comentalo
indir = r"C:\EODP_test_repo\EODP_test_repo\EODP-TS-E2E\Output_ISM_E2E_python311" #esto es para la ultima parte del report si no estamos en esa parte, comentalo
outdir = r"C:\EODP_test_repo\EODP_test_repo\EODP-TS-E2E\Output_L1B_E2E_python311" #esto es para la ultima parte del report si no estamos en esa parte, comentalo

# Initialise the ISM
myL1b = l1b(auxdir, indir, outdir)
myL1b.processModule()
