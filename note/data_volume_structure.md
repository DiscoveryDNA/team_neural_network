This file documents the structure of the data volume (the volume labeled `Yichen's new output`). The purpose of each subdirectory is detailed below:

- `complete_output`: It stores all one-hot encoded outputs with three motifs attached (`zelda`, `hb` and `bcd`). The outputs are stored as plain `txt` files that can be viewed directly. They are stored in format corresponding to Python lists, and can be parsed into Python lists with the `ast` package.
- `shelve`: It stores the `shelve` files that served as intermediate outputs in [producing_output_files_with_motif.ipynb](code/utility/producing_output_files_with_motif.ipynb) file. All files here are binary and should not be used externally.
- `10_percent`: It stores randomly selected subsets of the complete output. Each file in this directory consists of 10% of sequences in the complete output, all selected randomly. Each file is a `pickle` binary file so cannot be viewed directly, but it can be imported into a Python file as a list using the `pickle` package.
- `30_percent`: The same as `10_percent` with the exception that each file here consists of 30% of sequences in the complete output.
- `random_sequences`: This folder holds randomly generated pseudo-dna-sequence. It currently has two files, containing sequences of lengths 1000 and 5000 respectively.
