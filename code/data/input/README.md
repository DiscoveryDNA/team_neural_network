# README.md for data

## About

This is the directory for data. Data has been retrieved from 24 speices of fruit flies in the Montium clade. 

Example Fasta header:

`VT0847|1|dkik|-|2607`
- VT0847: Region ID
- 1: positive presence of expression 
- dkik: species ID
- -: read from the negative strand
- 2607: length of sequence in bp

## Directory 

`1.all_lifted_07March2018`: The is the raw data lifted from the genomes of 24 species. 
`2.outlier_removal_07March2018`: This data has processed using `QC_pipeline_4_kvon_outliers_1.R` (not present). Basically the program removed individual sequences based on length of the sequences. It found the mean length of all the sequences in each regions and established if there were any outliers.  All outliers that were less than the mean were removed. 
`3.species_24_only`: These are all sequences that passed the outlier removal step and had one and only one sequence per each of the 24 species.  These sequences were processed using shell tools.  