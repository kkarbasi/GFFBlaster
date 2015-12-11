# -*- coding: utf-8 -*-
"""
Created on Mon Dec 07 14:23:27 2015

@author: Kaveh
"""

from GFFBlaster import GFFBlaster
import sys
import os.path

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

def fill(text, width=70):
    return '\n'.join(text[i:i+width] for i in
                     range(0, len(text), width))

for i in range(gffb.getNumberOfSeqs()):
    for j in range(gffb.getNumberOfGenesInSeq(i)):
        print ">gi|"+sys.argv[1]+"|Gene "+ str(j)+ " of contig " + str(i)
        print fill(gffb.getGene(i,j),80)

        
        