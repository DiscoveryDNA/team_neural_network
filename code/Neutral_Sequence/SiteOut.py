#This program creates neutral spacer between sequences

#call this for patser to run properly
  #os.system("export MALLOC_CHECK_=0")

#usage: python siteout.py Pvalue GCcontent  SpGCcontent Sequences.txt motifs.txt



import os
import sys
import random
import string
import math
import re
#import pwm 
import csv
import numpy
#import pylab as plt
from matplotlib.backends.backend_pdf import PdfPages
from operator import itemgetter
from time import time


class BS:
  def __init__(self):

    self.strength = []
    self.start = []
    self.length = []
    self.sites=[]

  def reset(self):
    self.strength = []
    self.start = []
    self.length = []
    self.sites=[]
  
def FASTA(filename): #extract sequences from fasta file
    f = file(filename)

    order = []
    sequences = {}
    for line in f:
      if line.startswith('>'):
        name = line[1:].rstrip('\n')
        name = name.replace('_', ' ')
        order.append(name)
        sequences[name] = ''
      else:
        sequences[name] += line.rstrip('\n').rstrip('*')

    seqs = []
    

    for name in order:
      seqs.append(sequences[name].upper())


    return seqs

def findBStotal(TFBSold):
  BSold=0
  "this function gives the number of BSs removing duplicates"
  #find unique TF type from PWMs: ex. Bcd_whatever.pwm --> Bcd
  names = [None]*len(TFBSold.sites)
  for i in range(0,len(TFBSold.sites)):
    aux1=TFBSold.sites[i]
    aux2=aux1.split('_')
    names[i]=aux2[0]

  uniquenames=list(set(names)) #list of unique BS types
  nTFs = len(uniquenames)

  for i in range(0,nTFs):
    indexsites = [None]*len(TFBSold.sites)
    k=0
    for j in range(0,len(names)):
      if names[j]==uniquenames[i]:
        indexsites[k] = j
        k=k+1

    indexsites = [x for x in indexsites if x != None]
    starts = itemgetter(*indexsites)(TFBSold.start) #start sites of all TFs of type uniquenames[i]

    if isinstance( starts, int ):
      Nuniquestart=1
    elif len(starts)>1:
      Nuniquestart = len(list(set(starts)))
    elif len(starts)==0:
      Nuniquestart=0

    BSold = BSold + Nuniquestart
    #BSold=len(TFBSold.sites)
  return BSold

#-----------------------------------------------------------------------
def callpatser(A,TFBSold,pval,PWMgc):
  "this function calls patser"

  dirName = 'pwm'
  seqDir = 'SyntheticInput/'
  homeDir = './'
  gcContent = PWMgc #background GC content to compute PWM from freq. matrices
  minPValue = math.log(pval) 
  outputSuffix = '_sites.out'
  tempFile = 'out.tmp'

  fh = open(os.path.join(seqDir, 'sequence.txt'), 'w')
  fh.write('%s\n'%(A))
  fh.close()

  fh = open('fileName', 'w')
  fh.write('%s%s\n' % (seqDir, 'sequence.txt'))
  fh.close()

  fh = open('alphabet', 'w')
  fh.write('A:T\nC:G\n\n')
  fh.close()


  pwmFiles = os.listdir(dirName)
  for i in range(len(pwmFiles)):   
    pwmName = os.path.splitext(pwmFiles[i])[0]
    outputFile = '%s%s' % (pwmName, outputSuffix)
    #print "Current PWM: %s\n" % pwmName
    
    fh = open(os.path.join(dirName, pwmFiles[i]), 'r')
    fileString = "%s\n" % (''.join(fh.readlines()))
    fh.close()
        
    currPwm = pwm.fm.parse(fileString)
    wm = currPwm.weightMatrix(gcContent)
    wmString = '\n'.join(["%.4f\t%.4f\t%.4f\t%.4f" % (row[0], row[1], row[2], row[3]) for row in wm])
    
    fh = open('matrix', 'w')
    fh.write('A\tC\tG\tT\n')
    fh.write("%s\n" % wmString)
    fh.close()
    
    '''
    submit to patser
    -w = weight matrix, -v = vertical matrix, -p = print matrix, -f = filename, -c = complementary, -l = lower score threshold
    '''
    
    cutoff = 0
    os.system("patser/patser-v3b -w -v -p -f fileName -c -l %.4f > %s " % (cutoff, tempFile))
    
    #Filter with proper p-value cutoff.  Manual because patser lacks this option
    filteredLines = []
    fh = open(tempFile, 'r')
    for line in fh:
      lineRe = 'ln\(p-value\)=\s+(.+)'
      lineMatch = re.search(lineRe, line.strip())
      if (lineMatch and float(lineMatch.group(1)) < minPValue):
        filteredLines.append(line)
      elif (not lineMatch):
        filteredLines.append(line)
    fh.close()
    
    fh = open(outputFile, 'w')
    fh.write(''.join(filteredLines))
    fh.close()

  os.unlink('fileName')
  os.unlink('alphabet')
  os.unlink('matrix')
  os.unlink(tempFile)


  resultsDir = 'patser_output/'       
  os.system("mv -f *.out %s" % (resultsDir))

  #Takes a directory of patser results files and makes them csv's for use with inSite
  

  outputDir = homeDir 
  #print outputDir
  TFBSold.reset()
  

  #for each result file extract list of binding sites and convert to InSite format
  resultFiles = os.listdir(resultsDir)
  for elem in resultFiles:
    fh = open(os.path.join(resultsDir, elem), 'r')

	
    nameMatch = re.search('(\w+)\_', elem) #extract binding site name from file name
    pwmName = nameMatch.group(1)
    
    pwmWidth = 0 #default
	
    for line in fh:
      pwmWidthMatch = re.search('^width of the matrix.+?(\d+)', line.strip()) #check if line has width info
      if (pwmWidthMatch):
        pwmWidth = int(pwmWidthMatch.group(1)) #set actual pwm width
		
      lineRe = '(\w+?)\.txt\s+position=\s+(\d+).+score=\s+([\d\.]+)' #regex of patser output format
      lineMatch = re.search(lineRe, line.strip()) #check if line has binding site info

      if (lineMatch):  #if it has binding site        
        #now put binding site info in InSite format and save in 'seqs' holder

        TFBSold.sites.append(pwmName)
        TFBSold.start.append(int(lineMatch.group(2))-1)
        TFBSold.length.append(pwmWidth)
        TFBSold.strength.append(float(lineMatch.group(3)))
	#print	lineMatch.group(2)
	#print pwmName

    fh.close()

   #get findBStotal from the matlab file findBStotal.m  no por ahora

  return 


def findexpmotifs(A,TFBSold,BSold,motif):
    "this function finds explicits motifs given by user"

    j=len(TFBSold.start)
    for k in range(0,len(motif)):
      mstring = motif[k]

      runs = re.finditer(mstring, A)
      for match in runs:
        #print 'dentro'
        j=j+1
        motifstart=match.start()
        motiflength=match.end()-motifstart
        sitename='expmotif'+ str(k)
        TFBSold.start.append(motifstart)
        TFBSold.length.append(motiflength)
        TFBSold.strength.append(0)
        TFBSold.sites.append(sitename)
        #print  motif[k],TFBSold.sites[j-1], TFBSold.strength[j-1],TFBSold.start[j-1],TFBSold.length[j-1]
        BSold=BSold+1

#        print 'motifs encontrados', BSold
        
    return  BSold



# MONTE CARLO ----------------------------------------------------------------------------------------------------------
def main():

  t0=time()

  pval = float(sys.argv[1])
  gc = float(sys.argv[2])   #GCcontent
  PWMgc= 0.01*float(sys.argv[3])       #Species GCcontent
  fileseqs=str(sys.argv[4])
  print fileseqs

  print pval,gc,PWMgc,fileseqs

  Sintro = [] 
  t = [] 


#read files and store lines in a list
  with open(fileseqs) as f:
     lines = f.read().splitlines(0)

     for line in lines:
     	print line
        seq, typ = line.split(',')
        Sintro.append(seq)
        t.append(typ)


  print t
  print Sintro


  Sintro=filter(bool,Sintro)#remove empty slots caused by \n in the input files

  f.close()

  onmotif=0
  if len(sys.argv)>5 :
    filemotifs=str(sys.argv[5])
    onmotif=1
    motif = FASTA(filemotifs)

  
  p=[("C", int(gc/2)), ("G", int(gc/2)), ("A", (100-int(gc))/2), ("T", (100-int(gc))/2)]   #weights for randseq function
  choice="".join(x * y for x, y in p)
  
  A0=''
  tt=[]
  Sseq =[]
 
#generate sequence and determine which nucleotides are fixed (=1)

  for j in range (0,len(Sintro)):
    if Sintro[j].isdigit() :

      A=A0+''.join([random.choice(choice) for x in range(int(Sintro[j]))])
      tt.extend([int(t[j]) for i in range(int(Sintro[j]))])
 
    else :
      
      A=A0+Sintro[j]
      tt.extend([int(t[j]) for i in range(len(Sintro[j]))])
      Sseq.append(Sintro[j])
 
    A0=A

  print 'Initial sequence', A
  os.system("mkdir patser_output")
  os.system("mkdir SyntheticInput")

  TFBSold=BS()
  TFBSnew=BS()

  BStt=[]
  BSttint=[]
  BSs=[]

  BSold=0
  BSnew=0
  BSintrinsic=0

    
#BS in regions we will not modify

  if os.path.exists('pwm'):#if PWMs are provided, search for binding sites
    callpatser(A,TFBSold,pval,PWMgc) 
    BSold=findBStotal(TFBSold)
    BSold2=len(TFBSold.start)
  
  if (onmotif ==1 ) :   #if specific motifs are provided, search for binding sites
    BSold=findexpmotifs(A,TFBSold,BSold,motif)

  print BSold, 'total number BS'

  for j in range(0, len(TFBSold.start)):  #binding sites in non modifiable regions
   
    BStt=tt[TFBSold.start[j]:TFBSold.start[j]+TFBSold.length[j]]
    BSttint=numpy.asarray(BStt)

    if numpy.all(BSttint==1) :
        BSintrinsic=BSintrinsic+1



  print BSintrinsic,'intrinsic BS'



  BSs.append(BSold)
  
#monte carlo iteration
#iterate
  iteration=0
  if len(TFBSold.strength)>0:
    finish=False
  else:
    finish=True


  while not finish:  #monte carlo move


    iteration=iteration+1
    out=False
    B=A #save old sequence

    while not out:

      for j in range(0,len(TFBSold.start)): #for each bindign site (TFBS):

        #1)randomly choose one bp of the TFBS
        r=numpy.random.randint(TFBSold.start[j],TFBSold.start[j]+TFBSold.length[j]-1)
		
	# 2) replace element r in each TFBS found only if it belongs to a modifiable part
          
        if (tt[r]==0) :
          aux=''.join([random.choice(choice) for x in range(1)]) 
          Aaux=list(A)

          Aaux[r]=aux # substitute nucleotide r by aux
          A = "".join(Aaux)
       
          #run patser to check the new sequence
      if os.path.exists('pwm'):#if PWMs are provided          
        callpatser(A,TFBSnew,pval,PWMgc)
        BSnew=findBStotal(TFBSnew)
      else:
        BSnew=0

      if (onmotif ==1 ) :  #if explicit motifs are provided
        BSnew=findexpmotifs(A,TFBSnew,BSnew,motif) 
       
      if BSnew==0: #if no TFBS are found, finish (out=True)
        BSold=BSnew
        BSs.append(BSnew)
        
        out=True
        
      elif BSnew>0: #if there are still TFBS, compute acceptance probabilities and decide whether to keep or not the new sequence
        	
        Pbs=math.exp(BSold-BSnew)/(1+math.exp(BSold-BSnew)) #probability based on number of TFBS
        Ptot=Pbs  #total probability, other probabilites could be added here

        rando=numpy.random.uniform(0,1,1)
        
        if rando < Ptot or BSnew<1:    #accept move and exit         
          TFBSold.reset()
          TFBSold.start=TFBSnew.start
          TFBSold.length=TFBSnew.length
          TFBSold.sites=TFBSnew.sites
          TFBSold.strength=TFBSnew.strength
          TFBSnew.reset()
          BSold=BSnew
          BSs.append(BSold)
         
          out=True
    
        else:               #don't accept move
          A=B
    
        if (time()-t0)>42000:   #walltime, if code has been running longer than a walltime, finish
          out=True
          finish=True
    
    if (iteration > 100) :      #if number of Binding sites has not changed in 100 iterations, exit
      if all(BSs[j] == BSold for j in (iteration-100,iteration)):
        finish=True


    if ((BSold-BSintrinsic <1) or (iteration>10000)):   #if all BS have been removed or number of iterations is greater than 10000 exit
      finish=True


  t1=time()
#date sets the name os the sequence
  Seqname='sequence'#'NS'+"".join(bb)

#email text
  fh = open('output.txt', 'w')
  fh.write('Congratulations, the sequence you designed was created. \n')
  fh.write('Running time:%f seconds\n' % (t1-t0))
  if (t1-t0)>41999:
    fh.write(' YOU REACHED THE RUNTIME LIMIT!! \n')
  fh.write('Total number of motifs (including func. sequences):%s \n' % BSold)
  fh.write('Total number of motifs in modifiable sections:%s \n' % (BSold - BSintrinsic))
  fh.write('Final sequence >%s \n' % A)
  fh.write('A fasta file has been created in neutralseq.fa\n')
  fh.write('A .csv file has been created in sequence.csv, you can use it to visualize the binding site content of your sequence using InSite (http://www.cs.utah.edu/~miriah/insite/) \n')

  fh.close()

#save fasta file
  
  fh = open('neutralseq.fa', 'w')
  fh.write('>%s\n%s' % (Seqname,A))
  fh.close()
      

#run Zeba's script to create .csv file
  
  os.system('python patser2csv.py neutralseq.fa patser_output/ .')

  print 'Final sequence:', A
  print 'Total Binding sites:',  BSold
  print 'Intrinsic Binding sites:', BSintrinsic
  print 'Output written in file output.txt'
  print "DONE!"
		
  os.system('rm -r patser_output')
  os.system('rm -r SyntheticInput')



main()
