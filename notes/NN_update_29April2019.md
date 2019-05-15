# About

This document outlines the work that has been done along with current next steps for the Neural Network project. 

*note*: *This document is still under construction* - cm 5/12/19.

# 1. Bidirectional LSTM Data

## 1a. Original Montium Data Work

These datasets have been formatted and run to train Bi-directional LSTM. The PWM datasets are TFBS scores generated from [map_motif2](https://github.com/DiscoveryDNA/map_motif2). 

### Data
-	3,544 Regions from 24 species (85056) raw nucleotide sequences labeled as functional or non-functional according to Kvon 2013 [3__24_only_raw_07March2018](https://drive.google.com/open?id=183cIcoAjtZtnxIvlZ5wXkFvwLdKj6RTH) 
-	PWM Dataset 1 (bcd, cad, eve, zelda) [5_map_motif_no_threshold_14Nov2018](https://drive.google.com/open?id=19xUbC1KuxMBWwjveOtmyPKMYDc_dgoxQ)
-	PWM Dataset 2 ( hb, kni, kr, twi) [5_TFBS_scores_19March2019](https://drive.google.com/open?id=1PTmQwwgBzEDFNDVRdGMS8bn5gZgk8jJt)

### Experiments

-	First bi-directional [2019-01-29_shuffling_on_padding_at_the_end_with_size_1000_bidirectional.ipynb](https://github.com/DiscoveryDNA/team_neural_network/blob/master/code/experiments/2019-01-29_shuffling_on_padding_at_the_end_with_size_1000_bidirectional.ipynb)
	-	accuracy jumped to over 85%
	-	using only a subset of the data - a key point here is that the randomization process is not random sequences across all 3,544 sequences. Instead, we take the first ~200 regions, and randomly sample from that. That means that some of the regions are never represented in these first test models. 
	-	Only 4 TFBS (Dataset 1: bcd, cad, eve, zelda)
	-	Only on the positive strand 
-	Bi-directional with only nucleotide sequences [2019-02-04_shuffling_on_padding_at_the_end_with_size_1000_bidirectional_no_TFBS.ipynb](https://github.com/DiscoveryDNA/team_neural_network/blob/master/code/experiments/2019-02-04_shuffling_on_padding_at_the_end_with_size_1000_bidirectional_no_TFBS.ipynb)
	-	Accuracy 71%
-	Bi-directional without nucleotides, only TFBS scores [04_shuffling_on_padding_at_the_end_with_size_1000_bidirectional_only_TFBS.ipynb](https://github.com/DiscoveryDNA/team_neural_network/blob/master/code/experiments/2019-02-04_shuffling_on_padding_at_the_end_with_size_1000_bidirectional_only_TFBS.ipynb)
-	We did run on whole dataset [ ]()

## Control data

-	Random PWM of length (8,9,6,6) -  Mimics Dataset 1
-	[Random Sequences][https://drive.google.com/open?id=113Rztzwc0C1pAAQV2l9RUwkWkWkICAVC]
	- [ ] Need to learn a bit more about this data from Thomas. Where is his write up?
	- [ ] How many sequences do we have?
	- [ ] Need to run some tests to verify what Thomas says
	- [ ] Experiments 1. Need to run real PWM on them and train neural network with "random" functional assignments. 2. Use these sequences and run through most bi-directional model, need to get score on confidnece of if the sequence is functional or not. What kind of scores are we getting? We know a bit about the scores. Do the scores cluster with how the sequences were generated? This could tell us if the 
- [ ] 	Create Random alignments following a certain model of substituion using [pyvolve](https://github.com/sjspielman/pyvolve). This could be useful to test assumptions about the model reading similarity in sequence over the type of data.

## Cross Species Data

The importance of this data is overall to test the generality of the data beyond montium, but also to test how effective it is to use closely related species. 

- [ ] Just the D. mel sequences.
	- [ ] where are these?
- [ ] Get non-coding regions that are not in Kvon dataset from D.mel. So  Then perform liftover to gather the sequences. Using the `2.make2KBIntergenic.R` script, I made `1.random_intergenic_regions_1August2017.bed` and lifted them from all the montium genomes and Dmel. The sequences are located here: `Research2⁩/montium_analyses_1_alignment⁩/analyses_1_alignment⁩/pipeline_output_8⁩`
	- [ ] It looks as though it is picking one random 2kb region between each of the "intergenic regions"
	- [ ] It would be good to do a summary of these sequences.  
	- [ ] Is there overlap with Kvon?
	- [ ] What would we want to do with them?
-  [ ] Lifting across more thatn D.mel genomes.  Did we ever do this? What genomes can I get?


# Hybrid Model

- Add README to Hybrid Model 

This model is based of this paper: [ ]().  Basically the input is JUST the nucleotide sequences and it is run through a hybrid of ... and ....

## Experiments

- [Original Implementation](https://github.com/DiscoveryDNA/team_neural_network/blob/master/code/experiments/conv_rnn_hybrid_model/2019-3-22_tried_conv_rnn_hybrid_model.ipynb)
- [Motif Exraction](https://github.com/DiscoveryDNA/team_neural_network/blob/master/code/experiments/conv_rnn_hybrid_model/2019-4-13_motif_extracting.ipynb)
- [Train on Larger Dataset](https://github.com/DiscoveryDNA/team_neural_network/blob/master/code/experiments/conv_rnn_hybrid_model/train_on_larger_dataset.ipynb)


# Other TO-DO

- [ ] Earlier we experimented with adding padding to the front. Does this make a difference with the new bidirectional Architecture?
- [ ] What is the best way to save results of our accuracy, c-statistic, and FDR?

