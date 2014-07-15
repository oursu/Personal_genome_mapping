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
    
    parser.add_option('--gender_file',dest='gender_file',default='/srv/gs1/projects/snyder/jzaugg/histoneQTL/ChIPseq_alignment/data/metaData/20130606_sample_info.txt')
    parser.add_option('--out',dest='out',help='Out')
    parser.add_option('--genome_path',dest='genome_path',help='Genome path')
    parser.add_option('--vcf_path',dest='vcf_path',help='VCF path')
    parser.add_option('--align_dir',dest='alignment_directory',help='Alignment directory')
    parser.add_option('--people_data',dest='indir',help='Dir with individuals and data')
    opts,args=parser.parse_args()

    #check which individuals imputed
    imputed=set()
    seqCG=set()
    for line in open(opts.imputed,'r').readlines():
        items=line.strip().split()
        imputed_status=items[1]
        if imputed_status=='Imputed':
            imputed.add(items[0])
        if imputed_status=='Sequenced_CG':
            seqCG.add(items[0])
    print 'Imputed'
    print imputed
    print 'Sequenced CG'
    print seqCG

    #check which individuals are in the phase1 sequenced 1kgenomes.
    onek_vcf=open(opts.onek_vcf)
    for line in iter(onek_vcf):
        if '##' in line:
            continue
        if '#CHROM' in line:
            #this is line with individuals
            individuals=line.strip().split('\t')
            break
    print 'Sequenced'
    print individuals

    di={}
    #Add in fastq information for each id.
    for line in open(opts.k27,'r').readlines():
        items=line.strip().split('\t')
        sample_name=items[1]
        print sample_name
        #Some IDs are replicates, and their name will be NAxxxxx-d so we need to strip off the replicate number
        bam=items[0]
        if sample_name not in di.keys():
            di[sample_name]={}
        if 'H3K27AC' not in di[sample_name].keys():
            di[sample_name]['H3K27AC']={}
        di[sample_name]['H3K27AC']['read1']=bam.strip('pf.bam')+'1_pf.fastq.gz'
        di[sample_name]['H3K27AC']['read2']=bam.strip('pf.bam')+'2_pf.fastq.gz'
        di[sample_name]['H3K27AC']['AnalysisOutput']=os.path.basename(bam).strip('pf.bam')+'AnalysisOutput'
    for line in open(opts.k4me1,'r').readlines():
        items=line.strip().split('\t')
        sample_name=items[1]
        bam=items[0]
        if sample_name not in di.keys():
            di[sample_name]={}
        if 'H3K4ME1' not in di[sample_name].keys():
            di[sample_name]['H3K4ME1']={}
        di[sample_name]['H3K4ME1']['read1']=bam.strip('pf.bam')+'1_pf.fastq.gz'
        di[sample_name]['H3K4ME1']['read2']=bam.strip('pf.bam')+'2_pf.fastq.gz'
        di[sample_name]['H3K4ME1']['AnalysisOutput']=os.path.basename(bam).strip('pf.bam')+'AnalysisOutput'
    for line in open(opts.k4me3,'r').readlines():
        items=line.strip().split('\t')
        sample_name=items[1]
        bam=items[0]
        if sample_name not in di.keys():
            di[sample_name]={}
        if 'H3K4ME3' not in di[sample_name].keys():
            di[sample_name]['H3K4ME3']={}
        di[sample_name]['H3K4ME3']['read1']=bam.strip('pf.bam')+'1_pf.fastq.gz'
        di[sample_name]['H3K4ME3']['read2']=bam.strip('pf.bam')+'2_pf.fastq.gz'
        di[sample_name]['H3K4ME3']['AnalysisOutput']=os.path.basename(bam).strip('pf.bam')+'AnalysisOutput'
    #switch NA18870 with NA18505, based on Judith's suggestion                                                                                                            
    NA18870=di['NA18870'].copy()
    NA18505=di['NA18505'].copy()
    di['NA18870']=NA18505
    di['NA18505']=NA18870


    '''
    #Now, add in people from chromoVar paper
    for line in open(opts.prevPaper,'r').readlines():
        items=line.strip().split()
        celltype=items[3]
        reads=items[7]
        reads2=items[8]
        replicate=items[12]
        antibody=items[4]
        individual='NA'+celltype
        if individual not in di.keys():
            di[individual]={}
        if antibody.upper()=='H3K27AC':
            di[individual]=
    '''    


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

    #include by hand some people from chromoPaper
    gender_di['NASnyder']={}
    gender_di['NASnyder']['gender']='male'
    gender_di['NA19193']={}
    gender_di['NA19193']['gender']='female'
    gender_di['NA19194']={}
    gender_di['NA19194']['gender']='male'
    gender_di['NA2255']={}
    gender_di['NA2255']['gender']='male'
    gender_di['NA2588']={}
    gender_di['NA2588']['gender']='male'
    gender_di['NA2610']={}
    gender_di['NA2610']['gender']='male'
    gender_di['NA2630']={}
    gender_di['NA2630']['gender']='male'
    #print gender_di
    #Write the dictionary to a file
    out=open(opts.out,'w')
    #before, vcf was opts.vcf_path+imputed_prefix+id_name_for_info+'.vcf'
    vcf_universal='/srv/gs1/projects/snyder/jzaugg/histoneQTL/ChIPseq_alignment/data/genomes/mergedVCF/all_YRI_compiled/all_YRI_compiled.ALL_CHROMOSOMES.mergedAcrossSNPSources.final.vcf'
    imputed_genome_path='/srv/gs1/projects/snyder/jzaugg/histoneQTL/ChIPseq_alignment/data/genomes/imputedFasta'
    imputed_alignment_dir='/srv/gs1/projects/snyder/jzaugg/histoneQTL/ChIPseq_alignment/results/Alignments/imputed/'
    out.write('#Individual\tSampleName\tFQ1\tFQ2\tGenomePath\tGender\tVcfFile\tAlignmentDirectory\tSequencedOrImputed\n')
    for id_name in di.keys():
        genome_path=opts.genome_path
        alignment_directory=opts.alignment_directory
        print id_name
        id_name_for_info=id_name.split('-')[0]
        sequenced_or_imputed='NA'
        imputed_prefix=''
        if id_name_for_info in individuals:
            sequenced_or_imputed='S'
        elif id_name_for_info in imputed:
            sequenced_or_imputed='I'
            imputed_prefix='imputed'
            alignment_directory=imputed_alignment_dir
            genome_path=imputed_genome_path
        elif id_name_for_info in seqCG:
            sequenced_or_imputed='seqCG'
            imputed_prefix='seqCG'
            alignment_directory=imputed_alignment_dir
            genome_path=imputed_genome_path
        g='NA'
        if id_name_for_info in gender_di.keys():                                                                                                                         
            if 'gender' in gender_di[id_name_for_info].keys():  
                g=gender_di[id_name_for_info]['gender']
        print g
        if True:
            if 'H3K27AC' in di[id_name].keys():
                out.write(id_name_for_info+'\t'+id_name+'_H3K27AC'+'\t'+di[id_name]['H3K27AC']['read1']+'\t'+di[id_name]['H3K27AC']['read2']+'\t'+genome_path+'\t'+g+'\t'+vcf_universal+'\t'+alignment_directory+'\t'+sequenced_or_imputed+'\n')
            if 'H3K4ME1' in di[id_name].keys():
                out.write(id_name_for_info+'\t'+id_name+'_H3K4ME1'+'\t'+di[id_name]['H3K4ME1']['read1']+'\t'+di[id_name]['H3K4ME1']['read2']+'\t'+genome_path+'\t'+g+'\t'+vcf_universal+'\t'+alignment_directory+'\t'+sequenced_or_imputed+'\n')
            if 'H3K4ME3' in di[id_name].keys():
                out.write(id_name_for_info+'\t'+id_name+'_H3K4ME3'+'\t'+di[id_name]['H3K4ME3']['read1']+'\t'+di[id_name]['H3K4ME3']['read2']+'\t'+genome_path+'\t'+g+'\t'+vcf_universal+'\t'+alignment_directory+'\t'+sequenced_or_imputed+'\n')

    for line in open(opts.prevPaper,'r').readlines(): #chromopaper stuff
        items=line.strip().split()
        celltype=items[3]
        reads=items[7]
        reads2=items[8]
        replicate=items[12]
        antibody=items[4]
        if antibody not in ['H3K4me1','H3K4me3','H3K27Ac','Input']:
            continue
        if reads2=='NA':
            continue
        individual='NA'+celltype
        g='NA'
        if individual in gender_di.keys():
            g=gender_di[individual]['gender']
        sample_name='SNYDER_HG19_GM'+celltype+'_'+antibody.upper()+'_'+replicate
        if celltype=='Snyder':
            sample_name='SNYDER_HG19_SNYDER_'+antibody.upper()+'_'+replicate
        if 'INPUT' in sample_name:
            sample_name=re.sub('_1','',sample_name)
        out.write(individual+'\t'+sample_name+'\t'+reads+'\t'+reads2+'\t'+opts.genome_path+'\t'+g+'\t'+opts.vcf_path+'chromoPaper'+individual+'.vcf'+'\t'+opts.alignment_directory+'chromoVar_done_alignments/'+'\t'+'chromoPaper'+'\n')



main()
