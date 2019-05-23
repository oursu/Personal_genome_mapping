from optparse import OptionParser
import os,re
import math
from time import gmtime, strftime
import sys
'''
Mapping wrapper
Call the pipeline for mapping to personal genomes.
oursu@stanford.edu
'''

def main():
    parser=OptionParser()
    parser.add_option('--bashrc_file',dest='bashrc',help='Bashrc file',default='/srv/gsfs0/projects/kundaje/users/oursu/code/git_things/Personal_genome_mapping/personal_genome_mapping.bashrc')
    parser.add_option('--code_path',dest='code_path',help='Path of the code, to make it easy to transfer code and have it still work')
    parser.add_option('--metadata',dest='metadata',help='Metadata file. One line per condition. Should be tab or space-delimited: 1. Individual, 2. sample name (unique),3. fastq1, 4. fastq2, 5. genome_path (for instance for <path>/NA19099 the genome_path=path), 6. gender,7. vcf file for personal genome,alignment directory. If any of these entries is missing, e.g. fastq2 is missing, say NA. Header should start with #')
    parser.add_option('--step_to_perform',dest='step_to_perform',help='Step to perform. createGenome, alignBWA, alignTophat, reconcileBWA,reconcileTopHat, tagAlign. Here is what info each requires. vcf: Individual, vcf. createGenome: vcf, individual, gender and genome_path. align: individual, sample name, fastq1, fastq2,genome_path, alignment directory. reconcile: sample name, fastq1, fastq2, alignment_directory.  The rest of the items MUST BE PRESENT in the metadata file in the specified order, either as some actual values, or as the text NA to mark them.')
    parser.add_option('--sample_names_to_do',dest='todo',help='Sample names for subset of things to run',default='')
    parser.add_option('--fadir_male',dest='fadir_male',help='Fadir male',default='')
    parser.add_option('--genome_dict_male',dest='genome_dict_male',default='')
    parser.add_option('--BWAindex',dest='BWAindex',action='store_true')
    parser.add_option('--BowtieIndex',dest='BowtieIndex',action='store_true')
    parser.add_option('--gtf',dest='gtf',default='NA')
    parser.add_option('--trpref',dest='trpref',default='NA')
    parser.add_option('--chromo',dest='chromo',action='store_true',help='Whether to add "chr" in front of the vcf entries, so that they match the fasta files you are using')
    parser.add_option('--RNAnoveljuncs',dest='noveljuncs',action='store_true', help='set this if you want tophat run for RNA to include novel junctions.')
    opts,args=parser.parse_args()
    
    sample_di={}
    for line in open(opts.metadata).readlines():
        if line[0]=='#':
            continue
        items=line.strip().split()
        individual=items[0]
        fastq1=items[2]
        fastq2=items[3]
        sample_name=items[1]
        genome=items[4]
        gender=items[5]
        vcf_file=items[6]
        align_dir=items[7]
        if sample_name in sample_di.keys():
            sys.exit('Sample name '+sample_name+' appears multiple times in the metadata. Please recreate your metadata to have unique sample names')
        else:
            sample_di[sample_name]={}
            sample_di[sample_name]['sample_name']=sample_name
            sample_di[sample_name]['individual']=individual
            sample_di[sample_name]['fastq1']=fastq1
            sample_di[sample_name]['fastq2']=fastq2
            sample_di[sample_name]['genome_path']=genome
            sample_di[sample_name]['gender']=gender
            sample_di[sample_name]['vcf']=vcf_file
            sample_di[sample_name]['alignment_directory']=align_dir
    if opts.todo!='':
        of_interest=opts.todo.split(',')
    else:
        of_interest=sample_di.keys()
    print 'Focusing on these samples: '
    print of_interest

    #BUILD PERSONAL GENOME
    chromoadd=''
    if opts.chromo:
        chromoadd=' --chromo'
    done=set()
    if opts.step_to_perform=='createGenome':
        personal_genome_script=opts.code_path+'personalGenomeByIndividual.py'
        for sample_name in sample_di.keys():
            if sample_name not in of_interest:
                continue
            #If no vcf file, exit
            if sample_di[sample_name]['vcf']=='NA':
                sys.exit('No input vcf file for '+sample_name+'. Exiting ..')
            if sample_di[sample_name]['individual'] not in done:
                cmd='python '+personal_genome_script+' --addSNPtoFa --indiv '+sample_di[sample_name]['individual'].split('-')[0]+' --gender '+sample_di[sample_name]['gender']+' --vcf '+sample_di[sample_name]['vcf']+' --out_dir '+sample_di[sample_name]['genome_path']+'/'+' --fadir '+opts.fadir_male+' --genome_dict '+opts.genome_dict_male+' --code_path '+opts.code_path+chromoadd
                if opts.BWAindex:
                    cmd=cmd+' --BWAindex'
                if opts.BowtieIndex:
                    cmd=cmd+' --BowtieIndex'
                print cmd
                os.system(cmd)
                done.add(sample_di[sample_name]['individual'])
    
    #RECONCILE
    if opts.step_to_perform=='reconcileBWA':
        reconcile_script=opts.code_path+'new_ase_code/bin/reconcileBatch.sh'
        for sample_name in sample_di.keys():
            print 'checking if in of interest'
            print sample_name
            print sample_name in of_interest
            if sample_name not in of_interest:
                continue
            print 'ready to reconcile'
            info_file_reconcile=sample_di[sample_name]['alignment_directory']+'info_reconcile_'+sample_di[sample_name]['sample_name']
            make_info_file_reconcile='echo '+sample_di[sample_name]['sample_name']+' '+sample_di[sample_name]['fastq2']+' > '+info_file_reconcile
            os.system(make_info_file_reconcile)
            input_dir=sample_di[sample_name]['alignment_directory']
            output_dir=sample_di[sample_name]['alignment_directory']+'reconciled'
            os.system('mkdir '+output_dir)
            cmd=reconcile_script+' -i '+input_dir+' -o '+output_dir+' -l '+info_file_reconcile+' -s '+opts.bashrc
            os.system(cmd)
            print cmd
    if opts.step_to_perform=='reconcileTopHat':
        reconcile_script=opts.code_path+'new_ase_code/bin/reconcileRnaSample.sh'
        for sample_name in sample_di.keys():
            print sample_name
            print sample_name in of_interest
            if sample_name not in of_interest:
                continue
            print 'ready to reconcile'
            input_dir=sample_di[sample_name]['alignment_directory']+sample_name
            output_dir=sample_di[sample_name]['alignment_directory']
            os.system('mkdir '+output_dir)
            #--paired
            pairedend='0'
            if sample_di[sample_name]['fastq2']!='NA':
                pairedend='1'
            cmd=reconcile_script+' --indir '+input_dir+' --outdir '+output_dir+' --sample '+sample_name+' --sfile '+opts.bashrc+' --paired '+pairedend
            print cmd
            qsub_a_command(cmd,output_dir+'/'+sample_name+'_reconcileScript.sh','qqqq','20G')
            

    
    
    #ALIGN
    if opts.step_to_perform=='alignBWA':
        alignment_script=opts.code_path+'new_ase_code/bin/alignBatch.sh'
        for sample_name in sample_di.keys():
            if sample_name not in of_interest:
                continue
            if sample_di[sample_name]['alignment_directory']=='NA':
                sys.exit('No alignment directory provided for '+sample_name+'. Exiting ..')
            alignment_prefix=sample_di[sample_name]['alignment_directory']+sample_di[sample_name]['sample_name']
            #Make sure genome exists
            print sample_di[sample_name]['genome_path']+'/'+sample_di[sample_name]['individual'].split('-')[0]+'.maternal.bwt'
            if os.path.isfile(sample_di[sample_name]['genome_path']+'/'+sample_di[sample_name]['individual'].split('-')[0]+'.maternal.bwt'):
                #First, make the file required for alignBatch.sh
                print 'here'
                info_file=sample_di[sample_name]['alignment_directory']+'info_'+sample_di[sample_name]['sample_name']
                make_info='echo '+sample_di[sample_name]['sample_name']+' '+sample_di[sample_name]['individual'].split('-')[0]+' '+os.path.basename(sample_di[sample_name]['fastq1'])+' '+os.path.basename(sample_di[sample_name]['fastq2'])+' > '+info_file
                os.system(make_info)
                #Run alignment
                cmd=alignment_script+' -f '+os.path.dirname(sample_di[sample_name]['fastq1'])+' -b '+sample_di[sample_name]['alignment_directory']+' -s '+sample_di[sample_name]['genome_path']+' -l '+info_file+' -i '+opts.bashrc
                print cmd
                os.system(cmd)
                #print cmd

    #Get ready to align RNA
    if opts.step_to_perform=='alignTopHat':
        print "Ready to align with Tophat"
        print of_interest
        alignment_script=opts.code_path+'new_ase_code/bin/alignRnaSample_v2.sh'
        for sample_name in sample_di.keys():
            if sample_name not in of_interest:
                continue
            if sample_di[sample_name]['alignment_directory']=='NA':
                sys.exit('No alignment directory provided for '+sample_name+'. Exiting ..')
            alignment_prefix=sample_di[sample_name]['alignment_directory']+sample_di[sample_name]['sample_name']
            #Make sure genome exists                                                                                                                                                                                                                                                                               
            if os.path.isfile(sample_di[sample_name]['genome_path']+'/'+sample_di[sample_name]['individual'].split('-')[0]+'.maternal.1.bt2'):
                bamdir=sample_di[sample_name]['alignment_directory']+sample_name
                cmd=alignment_script+' --fq1 '+sample_di[sample_name]['fastq1']+' --fq2 '+sample_di[sample_name]['fastq2']+' --bamdir '+bamdir+' --mpref '+sample_name+'_maternal'+' --seqpref '+sample_di[sample_name]['genome_path']+'/'+sample_di[sample_name]['individual']+'.maternal'+' --trpref '+opts.trpref+' --gtf '+opts.gtf+' --sfile '+opts.bashrc+' -c'
                if opts.noveljuncs:
                    cmd=cmd+' -j'
                cmd2=re.sub('maternal','paternal',cmd)
                os.system('mkdir '+bamdir)
                print cmd
                print '----'
                print cmd2
                qsub_a_command(cmd+'qqqq'+cmd2,bamdir+'/'+sample_name+'_qsubscript.sh','qqqq','20G')

    #TAGALIGN
    if opts.step_to_perform=='tagAlign':
        tagAlign_script=opts.code_path+'remove_chrM_qc30_2tagAlign.sh'
        for sample_name in sample_di.keys():
            if sample_name not in of_interest:
                continue
            #aligned_person file
            dedup_dir=sample_di[sample_name]['alignment_directory']+'reconciled/dedup/'
            aligned_reconciled_deduped=sample_di[sample_name]['sample_name']+'_reconcile.dedup'
            outdir=sample_di[sample_name]['alignment_directory']+'tagAlign'
            os.system('mkdir '+outdir)
            cmd=tagAlign_script+' --indir '+dedup_dir+' --outdir '+outdir+' --sample '+aligned_reconciled_deduped
            print cmd
            qsub_a_command(cmd,outdir+'/'+aligned_reconciled_deduped+'_tagAlign_script.sh','qqqq','10G')

def qsub_a_command(cmd,shell_script_name,split_string=',',memory_number='20G'):
    f=open(shell_script_name,'w')
    cmds=cmd.split(split_string)
    for i in range(len(cmds)):
        f.write(cmds[i]+'\n') #just write the command
    f.close()
    #make runnable                                                                                                                                                      
    os.system('chmod 711 '+shell_script_name)
    #Qsub the script                                                                                                                                                    
    os.system("qsub -l mem_free="+memory_number+" -l h_vmem="+memory_number+" -l h_rt=20:00:00 -o "+shell_script_name+'.o'+' -e '+shell_script_name+'.e'+' '+shell_script_name)

main()
