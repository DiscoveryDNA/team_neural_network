"""Code for transforming the fasta DNA data into one hot encoding format."""

import os
from Bio import SeqIO

#Use the following dictionary to perform the transformation.
base_pairs = {'A': [True,False,False,False], 
'C': [False,True,True,True],
'G': [False,False,True,False],
'T': [False,False,False,True],
'a': [True,False,False,False],
'c': [False,True,False,False],
'g': [False,False,True,False],
't': [False,False,False,True],
'n': [False,False,False,False],
'N':[False,False,False,False]}
one_hot = []
file_num_limit = 110    #The maximum number of files to be decoded
file_count = 0

#Iterate through every file
for file in os.listdir("data/input/3.24_species_only"):
	#When the number of file decoded has reached the limit, stop.
	if (file_count < file_num_limit):
	    data = list(SeqIO.parse("data/input/3.24_species_only/" + file,"fasta"))
	    for n in range(0, len(data)):
	    	#Extract the header information
	    	header = data[n].description.split('|')
	    	regionID = header[0]
	    	expressed = header[1]
	    	speciesID = header[2]
	    	strand = header[3]
	    	#Complement all sequences in the negative DNA strand.
	    	if strand == '-':
	    		one_hot.append([expressed, speciesID, [base_pairs[n] for n in data[n].seq.complement()]])
	    	else:
	    		one_hot.append([expressed, speciesID, [base_pairs[n] for n in data[n].seq]])
	    output = open("data/output/" + regionID + ".txt", "w")
	    output.write(str(one_hot))
	    output.close()
	    file_count += 1
	else:
		break;