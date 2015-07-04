import os
import sys
sys.path.insert(1,'../headers/')
import file as fh
import numpy
import nibabel as nib   #provides read and write access to some common medical and neuro-imaging file formats
import cPickle
import mha
from brats_settings import *

###############################################

def generate_cubes():
	
	dirName = 'p' + str(plen) + 'o' + str(offset) + 'm' + str(mask)
	
	fh = open("output.txt", "a")#Output file for debugging
	
	if not os.path.exists(DATA_PATH + '/' + dirName):
		os.makedirs(DATA_PATH + '/' + dirName)

		#Read patients list
		patients = os.listdir(IM_PATH)

		#for patIdx in xrange(bratsPatients):
		for p in sorted(patients):
			#Patstr = str(patIdx+1).zfill(3)  #Padding the string with zeros on left
			#SeqStr = str(seqIdx+1).zfill(3)

			#truth = nib.load(TRUTH_PATH + '/' + p + '/masks/training' + Patstr + '_' + TimStr + '_mask' + str(mask) + '.nii').get_data()
			truthf = os.listdir(TRUTH_PATH+'/'+p)
			truth = mha.new(truthf)
			truth = truth.data

			shape = numpy.array(truth.size)
			numCubes = (shape - 2*(offset/2))/numPred  #numpred=plen-offset+1
			newShape = 2*(offset/2) + numCubes*numPred 
			cutOff = shape - newShape
			
			truthCrop = truth[cutOff[0]/2:cutOff[0]/2 + newShape[0],
							  cutOff[1]/2:cutOff[1]/2 + newShape[1],
							  cutOff[2]/2:cutOff[2]/2 + newShape[2]]


			SEQ_PATH = IM_PATH + '/' + p
			
			
					
			#Read sequences list
			files = os.listdir(SEQ_PATH)

			#for seqIdx in xrange(bratsSeqs):
			for i in range(bratsSeqs):
				f = sorted(files)[i]
				path = os.path.join(SEQ_PATH,f)

				if os.path.isfile(path):
					data = numpy.zeros([bratsChannels,newShape[0],newShape[1],newShape[2]],dtype = 'float32')
					#data[0,:,:,:] = nib.load(IM_PATH + '/training' + Patstr + '/' +  TimStr + '/N_training' + Patstr + '_' + TimStr + '_flair_pp.nii').get_data()[cutOff[0]/2:cutOff[0]/2 + newShape[0],cutOff[1]/2:cutOff[1]/2 + newShape[1],cutOff[2]/2:cutOff[2]/2 + newShape[2]]
					#data[1,:,:,:] = nib.load(IM_PATH + '/training' + Patstr + '/' +  TimStr + '/N_training' + Patstr + '_' + TimStr + '_mprage_pp.nii').get_data()[cutOff[0]/2:cutOff[0]/2 + newShape[0],cutOff[1]/2:cutOff[1]/2 + newShape[1],cutOff[2]/2:cutOff[2]/2 + newShape[2]]
					#data[2,:,:,:] = nib.load(IM_PATH + '/training' + Patstr + '/' +  TimStr + '/N_training' + Patstr + '_' + TimStr + '_pd_pp.nii').get_data()[cutOff[0]/2:cutOff[0]/2 + newShape[0],cutOff[1]/2:cutOff[1]/2 + newShape[1],cutOff[2]/2:cutOff[2]/2 + newShape[2]]
					#data[3,:,:,:] = nib.load(IM_PATH + '/training' + Patstr + '/' +  TimStr + '/N_training' + Patstr + '_' + TimStr + '_t2_pp.nii').get_data()[cutOff[0]/2:cutOff[0]/2 + newShape[0],cutOff[1]/2:cutOff[1]/2 + newShape[1],cutOff[2]/2:cutOff[2]/2 + newShape[2]]
					data[i,:,:,:] = f.get_data()[cutOff[0]/2:cutOff[0]/2 + newShape[0],cutOff[1]/2:cutOff[1]/2 + newShape[1],cutOff[2]/2:cutOff[2]/2 + newShape[2]]
			
			data = data.astype('float32')
					
			#count = 0
			dataList = []
			truthList = []
			
			for ix in xrange(numCubes[0]):
				startx = ix*numPred
				endx = startx + numPred + 2*(offset/2)
				for iy in xrange(numCubes[1]):
					starty = iy*numPred
					endy = starty + numPred + 2*(offset/2)
					for iz in xrange(numCubes[2]):
						startz = iz*numPred
						endz = startz + numPred + 2*(offset/2)
						
						tumourVoxels = numpy.array(truthCrop[startx+offset/2:endx-offset/2,starty+offset/2:endy-offset/2,startz+offset/2:endz-offset/2])
						#NtumourVoxels = numpy.sum(tumourVoxels)
						unique, counts = np.unique(tumourVoxels, return_counts=True)
						#y=numpy.asarray((unique)).T
						z=numpy.asarray((counts)).T
						sum=numpy.sum(z)
						if(sum > Threshold):									
							#count = count+1
							dataList.append(data[:,startx:endx,starty:endy,startz:endz])
							truthList.append(tumourVoxels)
			
			#data_file = file(DATA_PATH + '/' + dirName + '/pat_'+ Patstr + '_time_' + TimStr + '.pkl','wb')
			data_file = file(DATA_PATH + '/' + dirName + '/'+ p + '.pkl','wb')			
			truth_file = file(DATA_PATH + '/' + dirName + '/' + p + '_truth.pkl','wb')
			cPickle.dump(numpy.array(dataList),data_file,cPickle.HIGHEST_PROTOCOL)
			cPickle.dump(numpy.array(truthList),truth_file,cPickle.HIGHEST_PROTOCOL)
			data_file.close()
			truth_file.close()
			u= 'Pat ' + p + ' had ' + str(sum) + ' tumour cubes\n'
			
			fh.write(u)
		fh.close
			
if __name__ == '__main__':
    generate_cubes()