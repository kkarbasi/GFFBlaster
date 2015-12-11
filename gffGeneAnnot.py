# -*- coding: utf-8 -*-
"""
Created on Sun Dec 06 19:50:31 2015

@author: Kaveh
"""
import sys
import os
from Bio.Blast import NCBIXML
from GFFBlaster import GFFBlaster
import glob

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


    parseDir = sys.argv[3];
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
               start, stop = gffb.getGeneCoordinates(i,j);
               outString = "Contig " + str(i) + "|Start: " + str(start) + "|Stop: " + str(stop)+ " |------> "  +  blastRecord.alignments[0].title 
               if blastRecord.alignments[0].hsps:
                   outString = outString + "-------" +"identities: "+ str(blastRecord.alignments[0].hsps[0].identities) + "/" + str(blastRecord.alignments[0].hsps[0].align_length)
           print outString
    
