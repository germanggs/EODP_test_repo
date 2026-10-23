# MAIN FUNCTION TO CALL THE L1C MODULE

from l1c.src.l1c import l1c

auxdir = r"C:\EODP_test_repo\EODP_test_repo\auxiliary"

# Geometry and radiances supplied for the L1C exercise
#gm_dir = r"C:\EODP_test_repo\EODP_test_repo\EODP_TER_2021\EODP-TS-L1C\input\gm_alt100_act_150"
#l1b_dir = r"C:\EODP_test_repo\EODP_test_repo\EODP_TER_2021\EODP-TS-L1C\input\l1b_output"

gm_dir = r"C:\EODP_test_repo\EODP_test_repo\EODP-TS-E2E\gm_out" #esto es para la ultima parte del report si no estamos en esa parte, comentalo
l1b_dir = r"C:\EODP_test_repo\EODP_test_repo\EODP-TS-E2E\Output_L1B_E2E_python311" #esto es para la ultima parte del report si no estamos en esa parte, comentalo

# The existing initialisation expects two paths separated by a comma
indir = gm_dir + "," + l1b_dir

#outdir = r"C:\EODP_test_repo\EODP_test_repo\EODP_TER_2021\EODP-TS-L1C\Output_L1C_python311"
outdir = r"C:\EODP_test_repo\EODP_test_repo\EODP-TS-E2E\Output_L1C_E2E_python311" #esto es para la ultima parte del report si no estamos en esa parte, comentalo
# Initialise and run L1C once
myL1c = l1c(auxdir, indir, outdir)
myL1c.processModule()



