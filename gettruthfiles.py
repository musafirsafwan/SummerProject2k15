import shutil

input_path = 'brats2013\normhgg'
output_path = 'saf_sak-hgg'
input_path, patients, files = os.walk(input_path).next()


for p in patients[0]:

    #Read all sequences
	sequences = os.listdir(input_path+'\\'+p)
    
    for t in sequences:	
        
        if (t.endswith('.mha'):
			if('OT' in t):
				output_file = output_path + '\\'+p+'\\'+t
				input_file =  input_path+'\\'+p+'\\'+t
                output_base = output_path + '\\'+p
                if not os.path.exists(output_base):
                    os.makedirs(output_base)
				
			    shutil.copy(input_file,output_file)