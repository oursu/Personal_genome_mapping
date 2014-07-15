from optparse import OptionParser
import os
import math
from time import gmtime, strftime
import gzip
'''
Author:Oana Ursu
'''

def main():
    parser=OptionParser()
    
    parser.add_option('--fastq',dest='fastq',help='Fastq file')
    opts,args=parser.parse_args()

    line_lim=10000

    #Read in some lines and check fastq version
    if opts.fastq[len(opts.fastq)-3:len(opts.fastq)]=='.gz':
        fastq=gzip.open(opts.fastq)
    else:
        fastq=open(opts.fastq)
    count_lines=0
    seen=set()
    for line in iter(fastq):
        count_lines=count_lines+1
        if count_lines>line_lim:
            break
        if count_lines%4==0:
            for c in line.strip():
                seen.add(c)
    if '!' in seen:
        print 'Sanger'
        exit
    else:
        if '1' in seen:
            print 'Illumina_1_8'
            exit
        else:
            if ';' in seen:
                print 'Solexa'
                exit
            else:
                if 'A' in seen:
                    print 'Illumina_1_3'
                    exit
                else:
                    #it's Illumina 1.5, but we return 1.3, because they are almost identical, and for 1.5, we want to use the -I flag
                    #print 'Illumina_1_5'
                    print 'Illumina_1_3'
                    exit

main()
