from optparse import OptionParser
import os
import math
from time import gmtime, strftime
import gzip
import sys
import re
'''
Author:Oana Ursu
'''

def main():
    parser=OptionParser()
    parser.add_option('--out_vcf',dest='out_vcf',help='Out vcf')
    parser.add_option('--indiv',dest='indiv',help='Individual')
    parser.add_option('--vcf_data',dest='vcf_data',help='Location of VCF files for these individuals. These data are for all chromosomes.')
    #, default='/srv/gs1/projects/kundaje/oursu/Alignment/data/1000Genomes/VCF/ALL.chrAll.phase1_release_v3.20101123.snps_indels_svs.genotypes.vcf')
    opts,args=parser.parse_args()

    vcf_data=opts.vcf_data
    #read in first few lines to find the column of the desired individual
    header_recorded=False
    out_vcf=open(opts.out_vcf,'w')
    vcf=open(vcf_data)                                                                                                                             
    for line in iter(vcf):
        if line[0:2]=='##':
            if header_recorded==False:
                #out_vcf.write(line)
                print 'ok'
            continue
        elif line[0]=='#':
            header_recorded=True
            #take out buffy, lcl and blood identifiers, so we can match to name of individual
            line=re.sub('_lcl','',re.sub('_blood','',re.sub('_buffy','',line)))
            items=line.strip().split('\t')
            if opts.indiv in items:
                #find individual
                #items=line.strip().split('\t')
                try:
                    indiv_idx=items.index(opts.indiv)
                except:
                    print 'Individual '+opts.indiv+' not found'
                break
            else:
                sys.exit('Individual '+opts.indiv+' not found')

    print 'Individual number is '+str(indiv_idx)
    print items[indiv_idx]
    #convert to unix number
    indiv_column=indiv_idx+1

    #cut -f this person, then grep only things not 0|/0
    #cmd='cat '+vcf_data+' | cut -f1-9,'+str(indiv_column)+" | grep -v \"0[|/]0\" | awk '$apo'{if(match($4,/[ATCG][ATCG]+/)==0 && match($5,/[ATCG][ATCG]+/)==0) print}'$apo' >> "+ opts.out_vcf
    cmd="cat "+vcf_data+" | cut -f1-9,"+str(indiv_column)+" | awk '{if(match($4,/[ATCG][ATCG]+/)==0 && match($5,/[ATCG][ATCG]+/)==0) print}' >> "+ opts.out_vcf
    print cmd
    print opts.out_vcf+'script.sh'
    qsub_a_command(cmd,opts.out_vcf+'script.sh','qqqqqqq')

def qsub_a_command(cmd,shell_script_name,split_string=',',memory_number='20G'):
    #write a shell script (for reproducibility)                                                                                                                      
    f=open(shell_script_name,'w')
    #f.write("apo=\"'\"\n")
    cmds=cmd.split(split_string)
    print cmds
    for i in range(len(cmds)):
        #f.write("cmd"+str(i)+"='"+cmds[i]+"'"+'\n')
        #f.write('echo $cmd'+str(i)+'\n')
        #f.write('eval $cmd'+str(i)+'\n')
        f.write(cmd+'\n')
    f.close()
    #make runnable
    os.system('chmod 711 '+shell_script_name)
    #Qsub the script                                                                                                                                                  
    os.system("qsub -l mem_free="+memory_number+" -l h_vmem="+memory_number+" -l h_rt=20:00:00 -o "+shell_script_name+'.o'+' -e '+shell_script_name+'.e'+' '+shell_script_name)



main()
