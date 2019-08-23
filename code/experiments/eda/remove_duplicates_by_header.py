import sys
from Bio import SeqIO
import numpy as np

def sequence_cleaner(fasta_file):
    # Create our hash table to add the sequences
    data = list(SeqIO.parse(fasta_file, "fasta"))
    print(len(data))
    regionids = np.array([seq.description.split('|')[0] for seq in data])
    unique_regions, counts = np.unique(regionids, return_counts=True)
    counter = {regionid:0 for regionid in unique_regions}
    sequences = {}

    # Using the Biopython fasta parse we can read our fasta input
    for seq in data:
        # Take the header of current sequence
        header = seq.description
        regionid = seq.description.split('|')[0]
        if counter[regionid] == 0:
            sequences[header] = str(seq.seq).upper()
            counter[regionid] += 1

    # Write the clean sequences

    # Create a file in the same directory where you ran this script
    with open("clear_" + fasta_file, "w+") as output_file:
        # Just read the hash table and write on the file as a fasta format
        for header, seq in sequences.items():
            print(header)
            output_file.write(">" + header + "\n" + sequences[header] + "\n")

    print("CLEAN!!!\nPlease check clear_" + fasta_file)


userParameters = sys.argv[1:]

sequence_cleaner(userParameters[0])