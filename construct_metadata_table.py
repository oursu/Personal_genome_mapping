from optparse import OptionParser
import os
import math
from time import gmtime, strftime
import re
'''
Author:Oana Ursu
'''

def main():
    parser=OptionParser()
    parser.add_option('--GM_vs_NA',dest='gm_or_na')
    parser.add_option('--gender_file',dest='gender_file')
    parser.add_option('--out',dest='out',help='Out')
    parser.add_option('--genome_path',dest='genome_path',help='Genome path')
    parser.add_option('--vcf_file',dest='vcf_file',help='VCF file with all individuals')
    parser.add_option('--align_dir',dest='alignment_directory',help='Alignment directory')
    parser.add_option('--people_data',dest='people_data',help='Sample to fasta files. Col1 = sample (should include individual name either NA19099 or GM19099). Col2: fasta full path')
    opts,args=parser.parse_args()

    di={}
    #Add in fastq information for each id.
    for line in open(opts.people_data,'r').readlines():
        items=line.strip().split('\t')
        sample_name=items[0]
        
        person=re.compile(opts.gm_or_na+'[0-9]*').findall(re.sub("GM",opts.gm_or_na,sample_name))[0]
        fastq=items[1]
        if sample_name not in di.keys():
            di[sample_name]={}
            di[sample_name]['fastq']=list()
            di[sample_name]['person']=person
        di[sample_name]['fastq'].append(fastq)

    #Get ourselves the gender dictionary                                                                                                                                 

    gender_di={}
    for line in open(opts.gender_file,'r').readlines():
        items=line.strip().split('\t')
        person=items[0]
        gender=items[4]
        famid=items[1]
        popul=items[2]
        if person not in gender_di.keys():
            gender_di[person]={}
        if person in gender_di.keys():
            gender_di[person]['gender']=gender
            gender_di[person]['famid']=famid
            gender_di[person]['population']=popul

    #Write the dictionary to a file
    out=open(opts.out,'w')
    out.write('#Individual\tSampleName\tFQ1\tFQ2\tGenomePath\tGender\tVcfFile\tAlignmentDirectory\n')
    for id_name in di.keys():
        genome_path=opts.genome_path
        alignment_directory=opts.alignment_directory
        print id_name
        g='NA'
        if id_name in gender_di.keys():                                                                                                                         
            if 'gender' in gender_di[id_name].keys():  
                g=gender_di[id_name]['gender']
        print g
        fastqs=['NA','NA']
        print di[id_name]['fastq']
        for i in range(len(di[id_name]['fastq'])):
            fastqs[i]=di[id_name]['fastq'][i]
        print fastqs
        print di[id_name]
        out.write(di[id_name]['person']+'\t'+id_name+'\t'+fastqs[0]+'\t'+fastqs[1]+'\t'+opts.genome_path+'\t'+g+'\t'+opts.vcf_file+'\t'+opts.alignment_directory+'\n')

main()
