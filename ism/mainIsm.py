
# MAIN FUNCTION TO CALL THE ISM MODULE

from ism.src.ism import ism

# Directory - this is the common directory for the execution of the E2E, all modules
#auxdir = r'C:\\EODP_test_repo\\EODP_test_repo\\auxiliary'
#indir = r"C:\\EODP_test_repo\\EODP_test_repo\\EODP_TER_2021\\EODP-TS-ISM\\input\\gradient_alt100_act150"  # small scene
# outdir = r"C:\\EODP_test_repo\\EODP_test_repo\\EODP_TER_2021\\EODP-TS-ISM\\Output_ISM_python311"


auxdir = r"C:\EODP_test_repo\EODP_test_repo\auxiliary" #esto es para la ultima parte del report si no estamos en esa parte, comentalo
indir = r"C:\EODP_test_repo\EODP_test_repo\EODP-TS-E2E\sgm_out" #esto es para la ultima parte del report si no estamos en esa parte, comentalo
outdir = r"C:\EODP_test_repo\EODP_test_repo\EODP-TS-E2E\Output_ISM_E2E_python311" #esto es para la ultima parte del report si no estamos en esa parte, comentalo


# Initialise the ISM
myIsm = ism(auxdir, indir, outdir)
myIsm.processModule()
