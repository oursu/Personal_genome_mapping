from optparse import OptionParser
import os
import math
from time import gmtime, strftime
import gzip,sys
'''
Make vcf for imputed individuals.
'''

def main():
    parser=OptionParser()
    parser.add_option('--vcfdir',dest='vcf_dir',default='/srv/gs1/projects/snyder/jzaugg/histoneQTL/ChIPseq_alignment/data/genomes/imputed/VCF')
    parser.add_option('--do_imputed',action='store_true',dest='do_imputed', help='Get imputed genotyope')
    parser.add_option('--do_score',action='store_true',dest='do_score', help='Merge score with the dosages files')
    parser.add_option('--do_phasing',action='store_true',dest='do_phasing')
    parser.add_option('--info_threshold',dest='info_t',default='0.8')
    parser.add_option('--shapeit_output',dest='shapeit_output',default='/srv/gs1/projects/snyder/jzaugg/histoneQTL/ChIPseq_alignment/data/genomes/imputed/for_oana/shapeit_output/')
    parser.add_option('--impute2_compiled_dir',dest='impute2_compiled',default='/srv/gs1/projects/snyder/jzaugg/histoneQTL/ChIPseq_alignment/data/genomes/imputed/for_oana/impute2_compiled/')
    parser.add_option('--inputation_out',dest='outdir',default='/srv/gs1/projects/snyder/jzaugg/histoneQTL/ChIPseq_alignment/data/genomes/imputed/imputed_vcf')
    #parser.add_option('--metadata',dest='metadata',help='Metadata file. One line per condition. Should be tab or space-delimited: 1. Individual, 2. sample name (unique),3. fastq1, 4. fastq2, 5. genome_path (for instance for <path>/NA19099 the genome_path=path), 6. gender,7. vcf file for personal genome,alignment directory. If any of these entries is missing, e.g. fastq2 is missing, say NA. Header should start with #')
    opts,args=parser.parse_args()
    
    haplotype_pre='/srv/gs1/projects/snyder/jzaugg/histoneQTL/ChIPseq_alignment/data/genomes/imputed/for_oana/shapeit_output/YRI_trios_chr'
    haplotype_post='.haps'
    dosage_pre='/srv/gs1/projects/snyder/jzaugg/histoneQTL/ChIPseq_alignment/data/genomes/imputed/for_oana/impute2_compiled/YRI_subset_chr'
    dosage_post='.dosages.gz'

    os.system('mkdir '+opts.outdir)
    #==========
    #HAPLOTYPES
    #==========
    for chromosome in ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','X']:
        if not opts.do_phasing:
            continue
        
        if chromosome!="X":
            continue
        
        haplo_people={}
        people_counter=6
        for line in open(haplotype_pre+chromosome+'.sample','r').readlines()[2:]:
            person=line.strip().split()[1]
            haplo_people[person]=str(people_counter)+','+str(people_counter+1)
            people_counter=people_counter+2
        print haplo_people.keys()
        print len(haplo_people.keys())
        for person in haplo_people.keys():
            cmds=[]
            awk_cmd='awk \'$4 != "0" {print "chr'+chromosome+'\\t"$2"\\t"$1"\\t"$3"\\t"$4"\\t.\\t.\\t.\\tGT\\t"$5"|"$6}\''
            out=opts.outdir+'/'+os.path.basename(haplotype_pre)+chromosome+'_'+person+'.haps'
            outfile=open(out,'w')
            outfile.write('#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t'+person+'\n')
            outfile.close()
            cmd='cat '+haplotype_pre+chromosome+haplotype_post+' | cut -d " " -f2-5,'+haplo_people[person]+' | '+awk_cmd+' >> '+out
            cmds.append(cmd)
            if chromosome=='X':
                vcf_dir=opts.vcf_dir
                final_out=vcf_dir+'/'+person+'_chr'+chromosome+'.IMPUTED.vcf'
                vcf_header='/srv/gsfs0/projects/kundaje/users/oursu/code/personalGenomeAlignment/imputation_to_vcf/VCF_header_imputed'
                add_header='cat '+vcf_header+' > '+final_out
                cmd_vcf='cat '+out+' >> '+final_out
                cmds.append(add_header)
                cmds.append(cmd_vcf)
            print '\n'.join(cmds)
            qsub_a_command('qqqq'.join(cmds),out+'_script.sh','qqqq','3G')

    #=======
    #DOSAGES
    #=======
    #First, we remove the first part from the dosages and from the info file
    #cut -c5- 
    #Then we add in the score to the dosages file
    #Then we add the score to the resulting vcf
    #From the final vcf, we can filter by score metric.
    if opts.do_score:
        for chromosome in ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22']: #No chrX for imputation, only phasing
            '''
            if chromosome!='5':
                continue
            '''
            dosages_2=opts.outdir+'/'+os.path.basename(dosage_pre)+chromosome+'NoCol1'+dosage_post
            dosages_with_score=opts.outdir+'/'+os.path.basename(dosage_pre)+chromosome+'withScore.dosages.gz'
            dosage_vcf=opts.outdir+'/'+os.path.basename(dosage_pre)+chromosome+'withScore.dosages.almostVcf.gz'
            infofile=dosage_pre+chromosome+'.info'
            infofile2=opts.outdir+'/'+os.path.basename(dosage_pre)+chromosome+'NoCol1.info'
            remove_dosages_begin='zcat '+dosage_pre+chromosome+dosage_post+' | cut -d \' \' -f2- | sort > '+dosages_2
            remove_info_begin='cat '+infofile+' | cut -d \' \' -f2- | sort > '+infofile2
            add_score='join '+infofile2+' '+dosages_2+' | gzip > '+dosages_with_score
            cmds=[remove_dosages_begin,remove_info_begin,add_score]
            qsub_a_command('qqqq'.join(cmds),dosage_vcf+'_script.sh','qqqq','3G')
    for chromosome in ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22']:        
        '''
        if chromosome!='X':
            continue
        '''
        if not opts.do_imputed:
            continue
        print 'passed'
        dosage_people={}
        people_counter=13
        print dosage_pre+chromosome+'.sample'
        for line in open(dosage_pre+chromosome+'.sample','r').readlines()[2:]:
            print dosage_pre+chromosome+'.sample'
            items=line.strip().split()
            print items
            person=line.strip().split()[0]
            dosage_people[person]=str(people_counter)+','+str(people_counter+1)+','+str(people_counter+2)
            people_counter=people_counter+3
        dosage_with_score_cur=opts.outdir+'/'+os.path.basename(dosage_pre)+chromosome+'withScore.dosages.gz'
        for person in dosage_people.keys():
            print 'cmds'
            cmds=[]
            out_dosage=opts.outdir+'/'+os.path.basename(dosage_pre)+chromosome+'_'+person+'.dosages'
            outfile=open(out_dosage,'w')
            outfile.write('#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t'+person+'\n')
            outfile.close()
            awk_cmd='awk \'$5 != "0" {print "chr"'+chromosome+'"\\t"$3"\\t"$1"\\t"$4"\\t"$5"\\t"$2"\\t.\\t.\\tGT\\t"$6","$7","$8}\''
            cmd='zcat '+dosage_with_score_cur+' | grep -v D | grep -v I | cut -d " " -f1,5,10-12,'+dosage_people[person]+' | '+awk_cmd+' >> '+out_dosage
            cmds.append(cmd)
            #And replace with genotypes in the vcf, as well as filter by score through a complementary code.
            code='/srv/gsfs0/projects/kundaje/users/oursu/code/personalGenomeAlignment/imputation_to_vcf/ML_to_genotype.py'
            code_merge='/srv/gsfs0/projects/kundaje/users/oursu/code/personalGenomeAlignment/imputation_to_vcf/merge_phased_with_imputed.py'
            cmd2='python '+code+' --impute2_almostVCF '+out_dosage+' --out '+out_dosage+'.vcf'+' --info_threshold '+opts.info_t
            phased_vcf=opts.outdir+'/'+os.path.basename(haplotype_pre)+chromosome+'_'+person+'.haps'
            imputed_vcf=out_dosage+'.vcf'
            vcf_dir=opts.vcf_dir
            final_out=vcf_dir+'/'+person+'_chr'+chromosome+'.IMPUTED.vcf'
            os.system('mkdir '+vcf_dir)
            cmd3='python '+code_merge+' --phased '+phased_vcf+' --imputed '+imputed_vcf+' --out '+final_out+'.unsorted'
            cmds.append(cmd2)
            cmds.append(cmd3)
            #I better append the header here in the end, after I sort.
            vcf_header='/srv/gsfs0/projects/kundaje/users/oursu/code/personalGenomeAlignment/imputation_to_vcf/VCF_header_imputed'
            add_header='cat '+vcf_header+' > '+final_out
            cmds.append(add_header)
            sort_cmd='cat '+final_out+'.unsorted'+' | sort -n -k 2 >> '+final_out
            cmds.append(sort_cmd)
            qsub_a_command('qqqq'.join(cmds),final_out+'_script.sh','qqqq','20G')
    

def qsub_a_command(cmd,shell_script_name,split_string=',',memory_number='20G'):
    f=open(shell_script_name,'w')
    cmds=cmd.split(split_string)
    for i in range(len(cmds)):
        f.write(cmds[i]+'\n')
    f.close()
    os.system('chmod 711 '+shell_script_name)
    #Qsub the script                                                                                                                                                       
    os.system("qsub -l mem_free="+memory_number+" -l h_vmem="+memory_number+" -l h_rt=20:00:00 -o "+shell_script_name+'.o'+' -e '+shell_script_name+'.e'+' '+shell_script_name)



                


main()
