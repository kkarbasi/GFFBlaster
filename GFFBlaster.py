# -*- coding: utf-8 -*-
"""
Created on Fri Dec 04 14:04:54 2015

@author: Kaveh
"""

import sys
import os.path
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML


class GFFBlaster:
    def __init__(self , fastaData , gffData):
        self.fastaData = fastaData
        self.gffData = gffData
        self.seqGenes = []
        self.seqFasta = []
        self.seqHeaders = []
        self.parseData()
        
    def parseData(self):
        seqStartIndices = [i for i, ltr in enumerate(self.fastaData) if ltr == '>']
        # Check if there's at least one sequence (indicated by a '>' in its header) in the file
        if len(seqStartIndices) < 1:
            print 'No sequence found'
            exit()

        for  i,ind in enumerate(seqStartIndices):
            self.seqHeaders = self.seqHeaders + [self.fastaData[ind:self.fastaData[ind:].find('\n')+ind].rstrip("\n").lstrip("\n")]
            if i<len(seqStartIndices)-1:
                cur = self.fastaData[self.fastaData[ind:].find('\n')+ind:seqStartIndices[i+1]].rstrip("\n").lstrip("\n");
                cur = cur.replace('\n' , '').replace('\r' , '')
                self.seqFasta = self.seqFasta + [cur]
            else:
                cur = self.fastaData[self.fastaData[ind:].find('\n')+ind:].rstrip("\n").lstrip("\n")
                cur = cur.replace('\n' , '').replace('\r' , '')
                self.seqFasta = self.seqFasta + [cur]
                
                
        geneData = self.gffData.split('\n')
        geneSeqDel = geneData[0].rstrip('\n').lstrip('\n');
        self.seqGenes = self.gffData.split(geneSeqDel);
        self.seqGenes = self.seqGenes[1:]
        for i,dat in enumerate(self.seqGenes):
            self.seqGenes[i] = self.seqGenes[i].lstrip('\n').rstrip('\n')
            
            
    def getGeneCoordinates(self , seqNumber , geneNumber):
        '''
        Get gene coordinates of geneNumberth gene of the seqNumberth sequence
        '''
        start = int(self.getSeqGenes(seqNumber).split('\n')[geneNumber].split()[3]);
        stop = int(self.getSeqGenes(seqNumber).split('\n')[geneNumber].split()[4]);
        return start,stop
        
    def getSubSeq(self , seqNumber , start , stop):
        '''
        get sub sequence of the seqNumberth sequence starting from start ending in stop
        '''
        return self.seqFasta[seqNumber][start:stop]
        
    def getGene(self , seqNumber , geneNumber):
        '''
        Get geneNumberth gene of the seqNumberth sequence
        '''
        start , stop  = self.getGeneCoordinates(seqNumber , geneNumber);
        return self.getSubSeq(seqNumber , start , stop)
     
    
    def blastGene(self , seqNumber , geneNumber):
        seq = self.getGene(seqNumber , geneNumber);
        result_handle = NCBIWWW.qblast("blastn", "nr", seq , hitlist_size=1, expect = 50.0 , word_size = 28)
        return result_handle
        
    
        
    
    def getSeq(self , i):
        return self.seqFasta[i]
        
    def getHeader(self , i):
        return self.seqHeaders[i]
    
    
    def getSeqGenes(self , i):
        return self.seqGenes[i]
        
    def getNumberOfGenesInSeq(self, seqNumber):
        if not self.getSeqGenes(seqNumber):
            return 0
        return len(self.getSeqGenes(seqNumber).split('\n'))
    
    def getNumberOfSeqs(self):
        return len(self.seqGenes)

if __name__ == "__main__":
    
    if os.path.isfile(sys.argv[1]):
        infile = open(sys.argv[1])
        dataF = infile.read();
    else:
        print 'file does not exist or can\'t be opened'
        exit()
    
    if os.path.isfile(sys.argv[2]):
        infile = open(sys.argv[2])
        dataG = infile.read();
    else:
        print 'file does not exist or can\'t be opened'
        exit()
    
    gffb = GFFBlaster(dataF , dataG);
    '''
    print gffb.getHeader(0);
    
    print gffb.getGene(0,0)
    '''
    count = 0;
    print gffb.getNumberOfSeqs();
    print gffb.getNumberOfGenesInSeq(0)
    
    
    for i in range(gffb.getNumberOfSeqs()):
        for j in range(gffb.getNumberOfGenesInSeq(i)):
            count = count + 1
            results_hndl = gffb.blastGene(i,j);
            blast_records = NCBIXML.parse(results_hndl)
            print 'saving...',"my_blast-seq-" + str(i) + "-gene-" + str(j) + ".xml"
            save_file = open("my_blast-seq-" + str(i) + "-gene-" + str(j) + ".xml", "w")
            save_file.write(results_hndl.read())
            save_file.close()
            results_hndl.close()    

    
    print count


   
    
    
 