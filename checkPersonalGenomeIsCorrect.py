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
    parser.add_option('--fasta_1m',dest='fa_1m',help='Fasta file 1 of things to compare, maternal genome',
                      default='/srv/gs1/projects/snyder/jzaugg/histoneQTL/ChIPseq_alignment/data/genomes/Fasta/NA19099.maternal.fa')
    parser.add_option('--fasta_1p',dest='fa_1p',help='Fasta file 1 of things to compare, paternal genome',
                      default='/srv/gs1/projects/snyder/jzaugg/histoneQTL/ChIPseq_alignment/data/genomes/Fasta/NA19099.paternal.fa')
    #parser.add_option('--fasta_2m',dest='fa_2m',help='Fasta file 2 of things to compare, maternal genome',
    #                  default='/srv/gs1/projects/chromovar/rawdata/genomes/GM19099/GM19099.maternal.fa')
    #parser.add_option('--fasta_2p',dest='fa_2p',help='Fasta file 2 of things to compare, paternal genome',
    #                        default='/srv/gs1/projects/chromovar/rawdata/genomes/GM19099/GM19099.paternal.fa')
    parser.add_option('--out',dest='out',help='Out')
    parser.add_option('--vcf',dest='vcf',help='vcf file with positions of interest')
    parser.add_option('--paternal_only',dest='p_only',help='Check paternal only',action='store_true')
    parser.add_option('--maternal_only',dest='m_only',help='Check maternal only',action='store_true')
    opts,args=parser.parse_args()

    #out=open(opts.out,'w')
    #os.system('/srv/gs1/software/samtools/samtools-0.1.19/bin/samtools faidx '+opts.fa_1m)
    #os.system('/srv/gs1/software/samtools/samtools-0.1.19/bin/samtools faidx '+opts.fa_1p)
    '''
    for i in range(10000000):
        a=3
    #time.sleep(20)
    '''
    vcf=open(opts.vcf)
    '''
    fa1m=open(opts.fa_1m)
    for line in iter(fa1m):
        line_only=line.strip()
        for pos in range(len(line_only)):
            
        print len(line.strip())
    '''
    if opts.m_only==True:
        print 'maternal only'
        fa1m=pysam.Fastafile(opts.fa_1m)
        #fa2m=pysam.Fastafile(opts.fa_2m)
    if opts.p_only==True:
        print 'paternal only'
        fa1p=pysam.Fastafile(opts.fa_1p)
    if (not opts.m_only) and (not opts.p_only):
        fa1m=pysam.Fastafile(opts.fa_1m)
        fa1p=pysam.Fastafile(opts.fa_1p)
    #fa2p=pysam.Fastafile(opts.fa_2p)
    #print fa1m
    #fa1m_iter=pysam.tabix_iterator(fa1m)
    #r='chr21'
    #for r in ['chr1','chr2','chr3','chr4','chr4','chr5','chr6','chr7','chr8','chr9','chr10','chr11','chr12','chr13','chr14','chr15','chr16','chr17','chr18','chr19','chr20','chr21','chr22','chrX']:
    #i=0
    #print r
    #pos_base_1m='N'
    #pos_base_2m='N'
    #pos_base_1p='N'
    #pos_base_2p='N'
    correctGenome=True
    for line in iter(vcf):
        if '#' in line:
            continue
        if 'DEL' in line:
            continue
        #print '======'
        #print line
        items=line.strip().split('\t')
        #print items
        if len(items)<10:
            print 'not enough entries'
            print items
            continue
        chromo='chr'+items[0]
        #Understand the genotype from vcf
        alleles=[items[3],items[4]]
        if '0/0' not in items[9] and '0/1' not in items[9] and '1/0' not in items[9] and '1/1' not in items[9] and '0|1' not in items[9] and '0|0' not in items[9] and '1|0' not in items[9] and '1|1' not in items[9]:
            continue #this is fully unknown
        if items[9][1]=='/':
            continue #this is randomly phased, so we are not checking it for now
        if '\\' not in items[9] and '|' not in items[9] and '/' not in items[9]:
            continue #this is without genotype
        try:
            genotype=re.compile('[\d]\|[\d]').findall(items[9])[0].split('|')
        except:
            print items[9]
            print re.compile('[\d]\|[\d]').findall(items[9])
        seq_for_this=[alleles[int(genotype[0])],alleles[int(genotype[1])]]

        i=int(items[1])-1
        r=chromo
        pos_base_1m='initial'
        pos_base_1p='initial'
        if opts.m_only==True or (opts.m_only==False and opts.p_only==False):
            pos_base_1m=fa1m.fetch(r,i,i+1)
            #pos_base_2m=fa2m.fetch(r,i,i+1)
        if opts.p_only==True or (opts.m_only==False and opts.p_only==False):
            pos_base_1p=fa1p.fetch(r,i,i+1)
            #pos_base_2p=fa2p.fetch(r,i,i+1)

        f1set=[pos_base_1p.upper(),pos_base_1m.upper()]
        #f1set=[pos_base_1m.upper(),pos_base_1p.upper()]

        #print 'my set'
        #print f1set
        #print 'true'
        #print seq_for_this

        #f1set.append(pos_base_1m)
        #f1set.append(pos_base_1p)
        #f2set=set()
        #f2set.add(pos_base_2m)
        #f2set.add(pos_base_2p)
        if opts.m_only:
            if f1set[1]!=seq_for_this[1]:
                correctGenome=False
                out=open(opts.out+'_m_only_FAIL','w')
                out.write('M_ONLY Location in genome: '+r+': '+str(i)+' '+os.path.basename(opts.fa_1m)+' : '+pos_base_1m+'\n')
        if opts.p_only:
            if f1set[0]!=seq_for_this[0]:
                correctGenome=False
                out=open(opts.out+'_p_only_FAIL','w')
                out.write('P_ONLY Location in genome: '+r+': '+str(i)+' '+os.path.basename(opts.fa_1m)+' : '+pos_base_1m+'\n')
        if opts.m_only==False and opts.p_only==False:
            if f1set!=seq_for_this:
                correctGenome=False
                out=open(opts.out+'FAIL','w')
                out.write('Location in genome: '+r+': '+str(i)+' '+os.path.basename(opts.fa_1m)+' : '+pos_base_1m+' '+os.path.basename(opts.fa_1p)+' : '+pos_base_1p)
                print '====='
                print 'Location in genome: '+r+': '+str(i)+' '+os.path.basename(opts.fa_1m)+' : '+pos_base_1m+' '+os.path.basename(opts.fa_1p)+' : '+pos_base_1p
                print 'true'
                print seq_for_this
        
    if correctGenome:
        out=open(opts.out+'OK','w')
        out.write('Genome is in perfect agreement with its original vcf file.')


    

main()
