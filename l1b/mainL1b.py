
# MAIN FUNCTION TO CALL THE L1B MODULE

from l1b.src.l1b import l1b

# Directory - this is the common directory for the execution of the E2E, all modules
auxdir = r'C:\\EODP_test_repo\\EODP_test_repo\\auxiliary'
indir = r'C:\\EODP_test_repo\\EODP_test_repo\\EODP_TER_2021\\EODP-TS-L1B\\input'
outdir = r'C:\\EODP_test_repo\\EODP_test_repo\\EODP_TER_2021\\EODP-TS-L1B\\Output_German_2'

# Initialise the ISM
myL1b = l1b(auxdir, indir, outdir)
myL1b.processModule()
