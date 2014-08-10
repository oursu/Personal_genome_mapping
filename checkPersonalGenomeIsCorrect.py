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
    parser.add_option('--indiv',dest='indiv',help='Individual name')
    parser.add_option('--fasta_1m',dest='fa_1m',help='Fasta file 1 of things to compare, maternal genome')
    parser.add_option('--fasta_1p',dest='fa_1p',help='Fasta file 1 of things to compare, paternal genome')
    parser.add_option('--out',dest='out',help='Out')
    parser.add_option('--chrom',dest='chrom',action='store_true',help='Add "chr" to vcf')
    parser.add_option('--vcf',dest='vcf',help='vcf file with positions of interest')
    parser.add_option('--paternal_only',dest='p_only',help='Check paternal only',action='store_true',default=False)
    parser.add_option('--maternal_only',dest='m_only',help='Check maternal only',action='store_true',default=False)
    opts,args=parser.parse_args()

    vcf=open(opts.vcf)

    chromoadd=''
    if opts.chrom==True:
        chromoadd='chr'
    if opts.m_only==True:
        print 'maternal only'
        fa1m=pysam.Fastafile(opts.fa_1m)
    if opts.p_only==True:
        print 'paternal only'
        fa1p=pysam.Fastafile(opts.fa_1p)
    if (not opts.m_only) and (not opts.p_only):
        fa1m=pysam.Fastafile(opts.fa_1m)
        fa1p=pysam.Fastafile(opts.fa_1p)

    chromo_in_vcf_not_fasta=set()
    #Iterate through the vcf file and check correct incorporation of SNPs into genome, as long as these are phased
    correctGenome=True
    for line in iter(vcf):
        if '#' in line:
            if 'CHROM' in line:
                #Find the individual
                column_items=line.strip().split('\t')
                individual_column=column_items.index(opts.indiv)
                print column_items
                print column_items[individual_column]
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
        chromo=chromoadd+items[0]
        #Understand the genotype from vcf
        alleles=[items[3],items[4]]
        individual_value=items[individual_column]
        if '0/0' not in individual_value and '0/1' not in individual_value and '1/0' not in individual_value and '1/1' not in individual_value and '0|1' not in individual_value and '0|0' not in individual_value and individual_value not in individual_value and '1|1' not in individual_value:
            continue #this is fully unknown
        if individual_value[1]=='/':
            continue #this is randomly phased, so we are not checking it for now
        if '\\' not in individual_value and '|' not in individual_value and '/' not in individual_value:
            continue #this is without genotype
        try:
            genotype=re.compile('[\d]\|[\d]').findall(individual_value)[0].split('|')
        except:
            print individual_value
            print re.compile('[\d]\|[\d]').findall(individual_value)
        seq_for_this=[alleles[int(genotype[0])],alleles[int(genotype[1])]]

        i=int(items[1])-1
        r=chromo
        pos_base_1m='initial'
        pos_base_1p='initial'
        if opts.m_only==True or (opts.m_only==False and opts.p_only==False):
            pos_base_1m=fa1m.fetch(r,i,i+1)
            if fa1m.fetch(r,1,10)=='':
                chromo_in_vcf_not_fasta.add(r)
                continue
            #pos_base_2m=fa2m.fetch(r,i,i+1)
        if opts.p_only==True or (opts.m_only==False and opts.p_only==False):
            pos_base_1p=fa1p.fetch(r,i,i+1)
            if fa1p.fetch(r,1,10)=='':
                chromo_in_vcf_not_fasta.add(r)
                continue
            #pos_base_2p=fa2p.fetch(r,i,i+1)

        f1set=[pos_base_1p.upper(),pos_base_1m.upper()]
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
                out.write('True: '+str(seq_for_this))
                print '====='
                print 'Location in genome: '+r+': '+str(i)+' '+os.path.basename(opts.fa_1m)+' : '+pos_base_1m+' '+os.path.basename(opts.fa_1p)+' : '+pos_base_1p
                print 'true'
                print seq_for_this
    if len(chromo_in_vcf_not_fasta)>0:
        out=open(opts.out+'OK_missingChr','w')
        out.write("Warning: chromosomes below from the vcf were not found in the reference fasta")
        out.write(str(chromo_in_vcf_not_fasta))
    elif correctGenome:
        out=open(opts.out+'OK','w')
        out.write('Genome is in perfect agreement with its original vcf file.')


    

main()
