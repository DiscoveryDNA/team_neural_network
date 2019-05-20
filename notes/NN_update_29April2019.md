# About

This document outlines the work that has been done along with current next steps for the Neural Network project. 

*note*: *This document is still under construction* - cm 5/12/19.

# 1. Bidirectional LSTM Data

## 1a. Original Montium Data Work

These datasets have been formatted and run to train Bi-directional LSTM. The PWM datasets are TFBS scores generated from [map_motif2](https://github.com/DiscoveryDNA/map_motif2). 

### 1a. Data
-	3,544 Regions from 24 species (85056) raw nucleotide sequences labeled as functional or non-functional according to Kvon 2013 [3__24_only_raw_07March2018](https://drive.google.com/open?id=183cIcoAjtZtnxIvlZ5wXkFvwLdKj6RTH) 
-	PWM Dataset 1 (bcd, cad, eve, zelda) [5_map_motif_no_threshold_14Nov2018](https://drive.google.com/open?id=19xUbC1KuxMBWwjveOtmyPKMYDc_dgoxQ)
-	PWM Dataset 2 ( hb, kni, kr, twi) [5_TFBS_scores_19March2019](https://drive.google.com/open?id=1PTmQwwgBzEDFNDVRdGMS8bn5gZgk8jJt)

### 1a. Experiments

**Bi-directional Architecture**: These experiments led us to use the bidirectional archecture of the previous experiments which yielded much lower accuracy.

-	First bi-directional [2019-01-29_shuffling_on_padding_at_the_end_with_size_1000_bidirectional.ipynb](https://github.com/DiscoveryDNA/team_neural_network/blob/master/code/experiments/2019-01-29_shuffling_on_padding_at_the_end_with_size_1000_bidirectional.ipynb)
	-	accuracy jumped to over 85%
	-	using only a subset of the data - a key point here is that the randomization process is not random sequences across all 3,544 sequences. Instead, we take the first ~200 regions, and randomly sample from that. That means that some of the regions are never represented in these first test models. See "shuffling and subsetting" below.
	-	Only 4 TFBS (Dataset 1: bcd, cad, eve, zelda)
	-	Only on the positive strand 

**Shuffling and Subsetting**: These experiments tested how we subsetted our data for building models. We need to subset our data because if we used everything for every single model test, it would take too long. 

- Shuffling experiment 1: [ 2019-02-10_different_shuffling_order.ipynb](https://github.com/DiscoveryDNA/team_neural_network/blob/master/code/experiments/2019-02-10_different_shuffling_order.ipynb)
	- Previously, we sampled the training data from the whole data set. We accidentally found out that different ways to perform the sampling led to different results. Specifically, for the same amount of data and the same bidirectional LSTM model, the validation accuracy tend to be higher (around ~80%) if we obtained the training data by randomly sampling from the first few species. However, did the sampling to the whole data set to get the training data, the model gave a lower validation accuracy (around 57%). 
	- acc: 0.7095.  This significanly lowered the accuracy. We cannot just randomly grab sequences from all regions.  This hints at the possible lack of generatlity of our model.
- Shuffling 2: [2019-03-04_shuffling_on_padding_at_the_end_with_size_1000_bidirectional_bug_fix.ipynb](2019-03-04_shuffling_on_padding_at_the_end_with_size_1000_bidirectional_bug_fix.ipynb)
	-	The idea of this experiment is based on the understanding that any sequence bears more resemblance with its 23 'siblings' (which are next to each other in the list of sequences before shuffling). Without shuffling, either all siblings are in the training set, or all of them are in the validation set. By shuffling the sequences, all siblings would be randomly distributed into the training set and the validation set. We might be able to extract more information for a sequence based on those of its siblings that are distributed into the training set.
	-	[ ] In this experiment we use new data that includes the negative strand. ?? They did?
	-	acc: 0.8696
	-	Conclusion: To summarize, for any sequence, its most resemblance sequences are its 23 ‘siblings’. If we don’t shuffle the data, either all 24 ‘siblings’ are in the training data, or all of them are in the validation data. By shuffling them, the 24 ‘siblings’ are randomly distributed into both training and validation data, allowing us to extract more information.
-	Whole dataset [2019-02-10_whole_dataset_500_epochs.ipynb](https://github.com/DiscoveryDNA/team_neural_network/blob/master/code/experiments/2019-02-10_whole_dataset_500_epochs.ipynb)	

**Model Explainability** What components (TFBS vs Nucleotides) of the network are important for accuracy?

-	Bi-directional with only nucleotide sequences [2019-02-04_shuffling_on_padding_at_the_end_with_size_1000_bidirectional_no_TFBS.ipynb](https://github.com/DiscoveryDNA/team_neural_network/blob/master/code/experiments/2019-02-04_shuffling_on_padding_at_the_end_with_size_1000_bidirectional_no_TFBS.ipynb)
	-	This is testing how much the nucleotides add to the model.
	-	Accuracy 71%
-	Bi-directional without nucleotides, only TFBS scores [04_shuffling_on_padding_at_the_end_with_size_1000_bidirectional_only_TFBS.ipynb](https://github.com/DiscoveryDNA/team_neural_network/blob/master/code/experiments/2019-02-04_shuffling_on_padding_at_the_end_with_size_1000_bidirectional_only_TFBS.ipynb)
	-	This is testing how much TFBS scores add to the model. 
	-	acc: 0.8395
	-	Seems like the TFBS are the most important component, over nucleotides to the model.

**Adding more data**

- Adding more TFBS scores: [2019-04-06_new_data_with_size_1000_bidirectional.ipynb](https://github.com/DiscoveryDNA/team_neural_network/blob/master/code/experiments/2019-04-06_new_data_with_size_1000_bidirectional.ipynb)
	- Using  PWM Dataset 2 ( hb, kni, kr, twi) [5_TFBS_scores_19March2019](https://drive.google.com/open?id=1PTmQwwgBzEDFNDVRdGMS8bn5gZgk8jJt) and PWM Dataset 1 (bcd, cad, eve, zelda) [5_map_motif_no_threshold_14Nov2018](https://drive.google.com/open?id=19xUbC1KuxMBWwjveOtmyPKMYDc_dgoxQ).
	- acc: 0.9748 !!!
	- Seems like we are at a really good point in our network and should stop trying to increase accuracy, but likely should do parameter optimization and add positive scores. 

### 1b. To-Do Original Montium Data Experiments

- [ ] Parameter optimatization.  This mostly so we know that we are configuring our network correctly and most importantly learn how parameter optimization is performed. This is an important component to Neural Networks and we should all know the ins and outs.
- [ ] Add negative  scores.  This is just to be thorough. It doesn't really make sense to just include one strand or the other. While I don't really think it will affect the score, I think it is imporant to include this information. 

## 1b. Model Accuracy and Explainability i.e. Controls

The goal of these experiments is to understand what the model is telling us about the the data AND most imporantly, make sure that the data and features we are inputting are actually meaningul in a biological context. For example: Is the model learning something from the TFBS scores just because they are there and interpreting something that is not biologically real? 

### 1b. Data
-	Random PWM of length (8,9,6,6) -  Mimics Dataset 1
-	-  Random Sequences: [here](https://drive.google.com/drive/folders/113Rztzwc0C1pAAQV2l9RUwkWkWkICAVC).  These sequences were made using [neutral_sequence_generator](https://github.com/DiscoveryDNA/neutral_sequence_generator), which Creates a DNA sequence that has motifs distributed at a specified frequency seperated by a neutral sequence that purposefully does not contain the motifs. This program uses SiteOut which was developed by researchers at Harvard University. Motifs used: hb, bcd, cad, gt.
	- [ ] Need to learn a bit more about this data from Thomas. Where is his write up?
	- [ ] How many sequences do we have?
	- [ ] Need to run some tests to verify what Thomas says


### 1b. experiments
- Using random PWM on real data: [2019-04-25_new_data_with_size_1000_bidirectional_using_random_data.ipynb ](https://github.com/DiscoveryDNA/team_neural_network/blob/master/code/experiments/2019-04-25_new_data_with_size_1000_bidirectional_using_random_data.ipynb). Use the real nucleotides, with fake TFBS data. The "fake" PWM were the same length as PWM scores Dataset 1. 
	- val_acc: 0.5926
	- Bam. The "real" TFBS are important for identifying function over non-functional sequences. 

### 1b. To- Do "Control" Experiments

- [ ] Experiments Type 1. Need to run real PWM on them and train neural network with "random" functional assignments. 
- [ ] Experiment type 2. Use these sequences and run through most bi-directional model, need to get score on confidnece of if the sequence is functional or not. What kind of scores are we getting? We know a bit about the scores. Do the scores cluster with how the sequences were generated? 
- [ ] Another question I keep asking myself is, is the model just looking at sequence similarity and thats it? One way we could test this is to create alignments that were generated based on the Montium tree by simulating synthetic sequences along the tree, based on some sort of evoutional model. Create Random alignments following a certain model of substituion using [pyvolve](https://github.com/sjspielman/pyvolve). This could be useful to test assumptions about the model reading similarity in sequence over the type of data.

## Cross Species Data

The importance of this data is overall to test the generality of the data beyond Montium species, but also to test how effective it is to use closely related species. 

- [ ] Just the D. mel sequences.
	- [ ] where are these?
- [ ] Get non-coding regions that are not in Kvon dataset from D.mel. So  Then perform liftover to gather the sequences. Using the `2.make2KBIntergenic.R` script, I made `1.random_intergenic_regions_1August2017.bed` and lifted them from all the montium genomes and Dmel. The sequences are located here: `Research2⁩/montium_analyses_1_alignment⁩/analyses_1_alignment⁩/pipeline_output_8⁩`
	- [ ] It looks as though it is picking one random 2kb region between each of the "intergenic regions"
	- [ ] It would be good to do a summary of these sequences.  
	- [ ] Is there overlap with Kvon?
	- [ ] What would we want to do with them?
-  [ ] Lifting across more thatn D.mel genomes.  Did we ever do this? What genomes can I get?

# 2a. Hybrid Model

This model is based off the architecture used in thispaper: [DanQ: a hybrid convolutional and recurrent deep neural network for quantifying the function of DNA sequences ](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4914104/). The first layers of
the model are designed to scan sequences for motif sites through convolution filtering. It is called the hybrid model because it uses two types of architectures 1. The first layers of
the model are designed to scan sequences for motif sites through convolution filtering. 2.  a Recurrent layer (of the LSTM type) to try to discover a “grammar” for how these single motifs work together (a layer for looking at the distance between motifs).

This greatest part of this work is that it is able to input just the nucleotide sequences to understand how the model is predicting function. After the model is built, you can identify what each layer is doing, literally by finding the nucleotide position, then grabbing the sequences around that position. So you can input a group of sequences, then get a list of "motifs". There are some problems, in that you really don't know if the layer is considered "important" for the model prediction, you just know what the layer is looking at when predicting. 

-[ ]  Add README to Hybrid Model directory

## 2a. Experiments

- Intitial Data Prep and Architecture: [2019-3-22_tried_conv_rnn_hybrid_model.ipynb](https://github.com/DiscoveryDNA/team_neural_network/blob/master/code/experiments/conv_rnn_hybrid_model/2019-3-22_tried_conv_rnn_hybrid_model.ipynb) 
	- 	val_acc: 0.9023


#  Other TO-DO

- [ ] Earlier we experimented with adding padding to the front. Does this make a difference with the new bidirectional Architecture?
- [ ] What is the best way to save results of our accuracy, c-statistic, and FDR? I really need to scrap all this information from the experiments.
- [ ] How do we visualize all of this?

