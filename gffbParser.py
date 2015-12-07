# -*- coding: utf-8 -*-
"""
Created on Sun Dec 06 19:50:31 2015

@author: Kaveh
"""
import sys
from Bio.Blast import NCBIXML
import glob

if __name__ == "__main__":
    

    parseDir = sys.argv[1];
    nFiles = len(glob.glob(parseDir + "\\" + "*.xml"))
    
    nSeqs = len(glob.glob(parseDir + "\\" + "my_blast-seq-*-gene-0.xml"))
    
    #nGenes = len(glob.glob(sys.argv[3] + "\\" + "my_blast-seq-" + str(0) + "-gene-*.xml"))
    
    nGenes = []    
    for i in range(nSeqs):
        nGenes = nGenes + [len(glob.glob(parseDir + "\\" + "my_blast-seq-" + str(i) + "-gene-*.xml"))]
        
    print "Blast record title of:"
    for i in range(nSeqs):
        for j in range(nGenes[i]):
           blastRecFile = open(parseDir + "\\" + "my_blast-seq-" + str(i) + "-gene-" + str(j) + ".xml");
           blastRecord = NCBIXML.read(blastRecFile);
           if blastRecord.alignments:
               print "Gene " + str(j) + " of Sequence " + str(i)+ " ------> "  +  blastRecord.alignments[0].title 
    
    
