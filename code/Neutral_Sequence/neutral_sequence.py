import random
import os
from Bio import motifs

def distribution(length, probability):
	divisions = (length * probability) + 1
	length= length - (divisions * 8)
	rand_col = []
	for i in range(0, int(divisions)):
		rand_col.append(random.random())

	total = sum(rand_col)
	sum_k = []
	for j in rand_col:
		sum_k.append(round((j/total)*length))

	return sum_k

	



def motif_reader(path_name):
    motif_list =[]
    for filename in os.listdir(path_name):
        print(filename)
        with open(path_name + filename) as handle:
             word = motifs.read(handle, "pfm")
             handle.close()
        motif = str(word.consensus)
        print(motif)
        motif_list.append(motif)

    return motif_list


def motif_dist(motifs, probabilities, length):
	dist = []
	for i,j in zip(motifs,probabilities):
		repeats = round(j*length)
		for k in range(0, repeats):
			dist.append(i)
	
	random.shuffle(dist)
	print(dist)
	return dist




def write_seq_txt(dist, motifs):

	seq_txt = open("Sequences.txt", "w")
	for i in dist:
		
		
		try:
			mot = str(motifs.pop())
			seq_txt.write(mot+",")
			
		except:
			seq_txt.write('A'+",")
		seq_txt.write(str(i) + "")
		seq_txt.write("\n")

	seq_txt.close()

def write_motif_txt(motifs):
	mot_txt = open("motifs.txt", "w")
	print(len(motifs))
	for i in range(1, len(motifs)+1 ):
		mot_txt.write("> motif" + str(i))
		mot_txt.write("\n")
		mot_txt.write(motifs[i-1])
		mot_txt.write("\n")
	mot_txt.close()

import subprocess
def siteout_call():
	script = ["C:/Python27/python.exe", "siteout.py", ".5", "50.0", "Sequences.txt","motifs.txt"]
	process = subprocess.run("C:/Python27/python.exe siteout.py .05 .5 50.0 Sequences.txt motifs.txt")





def main(length, probabilities, GC_percent=50.0):

	motifs = motif_reader("C:/Users/Lanes/ResearchLab/team_neural_network/data/input/motif_pfm/")
	motif_list = motif_dist(motifs,probabilities, length)
	print(motif_list)
	numbers = distribution(length, sum(probabilities))
	print(numbers)
	write_seq_txt(numbers, motif_list)
	write_motif_txt(motifs)
	siteout_call()
	

main(10000,[.001,.005,.002,.005] )
