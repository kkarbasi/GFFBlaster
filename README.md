# GFFBlaster
A script to automatically BLASTs unknown genes in a gff format from an unknown sequence file in FASTA format and save the first returned records as XML files

Usage:
$ GFFBlaster [FASTA file name] [GFF file name]


The gffbParser file is a simple parser for xml outputs of the GFFBlaster:
Usage:
$ gffbParser [Directory path of xml output files] 