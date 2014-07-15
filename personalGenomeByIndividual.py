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
    
    parser.add_option('--python_path',dest='python_path',help='Python path. DEFAULT=/srv/gsfs0/projects/kundaje/users/oursu/code/python_2.7.6',
                      default='/srv/gsfs0/projects/kundaje/users/oursu/code/python_2.7.6')
    parser.add_option('--code_path',dest='code_path',help='Code path.',default='/srv/gsfs0/projects/kundaje/users/oursu/code/personalGenomeAlignment/')
    parser.add_option('--addSNPtoFa',dest='addSNP',action='store_true')
    parser.add_option('--BWAindex',dest='BWAindex',action='store_true')
    #parser.add_option('--check_genome_by_vcf',dest='BWAindex',action='store_true')
    parser.add_option('--out_dir',dest='out_dir',help='Directory for writing the personal genome')
    parser.add_option('--vcf',dest='vcf',help='Location of big vcf file')
    parser.add_option('--indiv',dest='indiv',help='Individual: format is like NA19099')
    parser.add_option('--gender',dest='gender',help='Individual gender. Genomes used are the ones from ENCODE. They can be found at /srv/gs1/projects/kundaje/oursu/Alignment/data/ENCODE_genomes/ .DEFAULT: female',default='female')
    opts,args=parser.parse_args()
    
    if opts.gender=='female':
        fadir='/srv/gs1/projects/kundaje/oursu/Alignment/data/ENCODE_genomes/female/'
        genome_dict='/srv/gs1/projects/kundaje/oursu/Alignment/data/ENCODE_genomes/female/ref.fa.fai'
    elif opts.gender=='male':
        fadir='/srv/gs1/projects/kundaje/oursu/Alignment/data/ENCODE_genomes/male/'
        genome_dict='/srv/gs1/projects/kundaje/oursu/Alignment/data/ENCODE_genomes/male/ref.fa.fai'
    #out_genome=opts.out_dir+'/'+opts.indiv

    total_cmds=[]
    individual_prefix=opts.out_dir+opts.indiv

    #=============================
    # ADD SNPS TO REFERENCE GENOME
    #=============================
    addSNP_cmd=opts.python_path+' '+opts.code_path+'new_ase_code/ase/python/addSnpsToFa.py --vcf '+opts.vcf+' --unphased '+individual_prefix+'.unphased '+fadir+' '+genome_dict+' '+individual_prefix+' '+opts.indiv
    #if opts.gender=='female':
    #    #addSNP_cmd=addSNP_cmd+' -f '
    check_genome='/srv/gs1/software/python/2.7/bin/python'+' '+opts.code_path+'checkPersonalGenomeIsCorrect.py --fasta_1m '+individual_prefix+'.maternal.fa'+' --fasta_1p '+individual_prefix+'.paternal.fa'+' --out '+individual_prefix+'_GenomeCorrect'+' --vcf '+opts.vcf
    print check_genome
    if opts.addSNP:
        total_cmds.append(addSNP_cmd)
        total_cmds.append('/srv/gs1/software/samtools/samtools-0.1.19/bin/samtools faidx '+individual_prefix+'.paternal.fa')
        total_cmds.append('/srv/gs1/software/samtools/samtools-0.1.19/bin/samtools faidx '+individual_prefix+'.maternal.fa')
        total_cmds.append(check_genome)
    #========================
    # MAKE GENOME IDX FOR BWA
    #========================
    BWAindex_cmd=opts.code_path+'new_ase_code/ase/bin/createBwaIdx.sh -i '+'/'+opts.out_dir.strip('/')+' -x bwa -e '+opts.indiv

    if opts.BWAindex:
        total_cmds.append(BWAindex_cmd)

    os.system('mkdir '+opts.out_dir+'/scripts')
    qsub_a_command('qqqqq'.join(total_cmds),opts.out_dir+'/scripts/'+opts.indiv+"personalGenomeByIndividual.sh",'qqqqq','20G')

def qsub_a_command(cmd,shell_script_name,split_string=',',memory_number='20G'):
    #write a shell script (for reproducibility)
    f=open(shell_script_name,'w')
    #f.write("apo=\"'\"\n")
    cmds=cmd.split(split_string)
    print cmds
    for i in range(len(cmds)):
        f.write("cmd"+str(i)+"='"+cmds[i]+"'"+'\n')
        f.write('echo $cmd'+str(i)+'\n')
        f.write('eval $cmd'+str(i)+'\n')
    f.close()
    #make runnable
    os.system('chmod 711 '+shell_script_name)
    #Qsub the script
    os.system("qsub -l mem_free="+memory_number+" -l h_vmem="+memory_number+" -l h_rt=40:00:00 -o "+shell_script_name+'.o'+' -e '+shell_script_name+'.e'+' '+shell_script_name)

main()
