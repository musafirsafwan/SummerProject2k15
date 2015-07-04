IM_PATH = '/media/brain/1A34723D34721BC7/MSE_BRATS/BRATS2014_training_preprocessed/Patients'
TRUTH_PATH = '/media/brain/1A34723D34721BC7/MSE_BRATS/truth_files'
DATA_PATH = '/media/brain/1A34723D34721BC7/MSE_BRATS/cubes_generated'

numPred = 18
offset = 19
Threshold = 30

numPatients = 5
bratsPatients = 213

bratsSeqs = 4 #brats sequences

Tstamps = (1,1,1,1,1)
MSTstamps = (4,4,5,4,4)

numChannels = 4
bratsChannels = 4 #brats sequences?

mask = 2
plen = numPred + offset -1

valid_pat_num = 2					#Validation happens for all tstamps irrespective of training happens on all tstamps or not
img_shape = (181,217,181)
num_classes = 2 

test_pat_num = 5
test_tstamp = 1