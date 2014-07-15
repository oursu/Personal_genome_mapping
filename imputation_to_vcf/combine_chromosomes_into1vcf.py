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
    parser.add_option('--indir',dest='indir',default='/srv/gs1/projects/snyder/jzaugg/histoneQTL/ChIPseq_alignment/data/genomes/imputed/VCF/')
    parser.add_option('--vcf_dir',dest='vcf_dir',default='/srv/gs1/projects/snyder/jzaugg/histoneQTL/ChIPseq_alignment/data/genomes/VCF')
    parser.add_option('--metadata',dest='metadata',default='/srv/gs1/projects/snyder/jzaugg/histoneQTL/ChIPseq_alignment/data/metaData/fullMetaData_forAlignment.IMPUTED')
    opts,args=parser.parse_args()
    
    people=set()
    for line in open(opts.metadata,'r').readlines():
        person=line.strip().split('\t')[0]
        people.add(person)
    for person in people:
        cmd='cat '+opts.indir+person+'_chr*.IMPUTED.vcf'+' > '+opts.vcf_dir+'/imputed'+person+'.vcf'
        qsub_a_command(cmd,opts.vcf_dir+'/imputed'+person+'.vcf_script.sh',split_string=',',memory_number='20G')

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
