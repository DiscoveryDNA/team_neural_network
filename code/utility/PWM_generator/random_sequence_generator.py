import random
from Bio import motifs
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO
import os
import neutral_sequence

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


def sequence_generator(length, motif_frequencies):

    write=[]
    for _ in range(0,24):

        neutral_sequence.main(length,motif_frequencies)

        generated_sequence = SeqIO.read("neutralseq.fa", "fasta")
        generated_sequence = generated_sequence.seq
        

        
        enhancer = str(random.randint(0,1))
        output = SeqRecord(generated_sequence, id=str(_)+'|'+enhancer, name="random", description="This is a randomly generated sequence")
        write.append(output)

    SeqIO.write(write, "my_example.faa", "fasta")

sequence_generator(10000,[.001,.005,.002,.005])