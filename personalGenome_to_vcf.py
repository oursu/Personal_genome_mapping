from optparse import OptionParser
import os
import math,re
from time import gmtime, strftime
import pysam
import pickle
import subprocess
import gzip
'''
Author:Oana Ursu
'''

def main():
    parser=OptionParser()    
    parser.add_option('--fasta_1m',dest='fa_1m',help='Fasta file 1 maternal more or less',
                      default='/srv/gs1/projects/snyder/jzaugg/histoneQTL/ChIPseq_alignment/data/genomes/Fasta/NA19099.maternal.fa')
    parser.add_option('--fasta_1p',dest='fa_1p',help='Fasta file 1 paternal more or less',
                      default='/srv/gs1/projects/snyder/jzaugg/histoneQTL/ChIPseq_alignment/data/genomes/Fasta/NA19099.paternal.fa')
    parser.add_option('--out',dest='out',help='Out')
    parser.add_option('--indiv',dest='indiv',help='Name of individual (for column name in vcf)')
    parser.add_option('--vcf',dest='vcf',help='vcf file with positions of interest')
    opts,args=parser.parse_args()


    vcf=open(opts.vcf)
    new_vcf=open(opts.out,'w')
   
    fa1m=pysam.Fastafile(opts.fa_1m)
    fa1p=pysam.Fastafile(opts.fa_1p)

    #line_c=0
    for line in iter(vcf):
        #line_c=line_c+1
        #if line_c>100:
        #    break
        if '##' in line:
            new_vcf.write(line)
            continue
        if 'DEL' in line:
            continue
        if '#CHROM' in line:
            items=line.strip().split('\t')
            new_vcf.write('\t'.join(items[0:9])+'\t'+opts.indiv+'\n')
            continue
        items=line.strip().split('\t')
        #print items
        if len(items)<9:
            continue
        chromo='chr'+items[0]
        #Understand the genotype from vcf
        alleles=[items[3],items[4]]
        #genotype=re.compile('[\d]\|[\d]').findall(items[9])[0].split('|')
        #seq_for_this=[alleles[int(genotype[0])],alleles[int(genotype[1])]]

        i=int(items[1])-1
        r=chromo
        pos_base_1m=fa1m.fetch(r,i,i+1)
        pos_base_1p=fa1p.fetch(r,i,i+1)

        genotype_from_genome=[pos_base_1p.upper(),pos_base_1m.upper()]
        #write down 0|1 type genotype as learned from the genome
        first='.'
        second='.'
        if genotype_from_genome[0]==alleles[0]:
            first='0'
        elif genotype_from_genome[0]==alleles[1]:
            first='1'
        if genotype_from_genome[1]==alleles[0]:
            second='0'
        elif genotype_from_genome[1]==alleles[1]:
            second='1'
        new_vcf.write('\t'.join(items[0:9])+'\t'+first+'|'+second+'\n')
    

main()
