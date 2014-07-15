from optparse import OptionParser
import os
import math
from time import gmtime, strftime

'''
Author:Oana Ursu
Call the pipeline steps for each sample in the dataset.
'''

def main():
    parser=OptionParser()
    
    parser.add_option('--code_path',dest='code_path',help='Path of the code, to make it easy to transfer code and have it still work')
    parser.add_option('--metadata',dest='metadata',help='Metadata file. One line per condition. Should be tab or space-delimited: 1. Individual, 2. sample name (unique),3. fastq1, 4. fastq2, 5. genome_path (for instance for <path>/NA19099 the genome_path=path), 6. gender,7. vcf file for personal genome,alignment directory. If any of these entries is missing, e.g. fastq2 is missing, say NA. Header should start with #')
    parser.add_option('--step_to_perform',dest='step_to_perform',help='Step to perform. vcf,createGenome, align, reconcile, tagAlign. Here is what info each requires. vcf: Individual, vcf. createGenome: vcf, individual, gender and genome_path. align: individual, sample name, fastq1, fastq2,genome_path, alignment directory. reconcile: sample name, fastq1, fastq2, alignment_directory.  The rest of the items MUST BE PRESENT in the metadata file in the specified order, either as some actual values, or as the text NA to mark them.')
    parser.add_option('--sample_names_to_do',dest='todo',help='Sample names for subset of things to run',default='')
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
    print 'Focusing on these samples: '+of_interest

    #BUILD PERSONAL GENOME
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
                cmd='python '+personal_genome_script+' --addSNPtoFa --BWAindex --indiv '+sample_di[sample_name]['individual'].split('-')[0]+' --gender '+sample_di[sample_name]['gender']+' --vcf '+sample_di[sample_name]['vcf']+' --out_dir '+sample_di[sample_name]['genome_path']+'/'
                print cmd
                os.system(cmd)
                done.add(sample_di[sample_name]['individual'])
    
    #RECONCILE
    if opts.step_to_perform=='reconcile':
        reconcile_script=opts.code_path+'new_ase_code/ase/bin/reconcileBatch.sh'
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
            cmd=reconcile_script+' -i '+input_dir+' -o '+output_dir+' -l '+info_file_reconcile
            os.system(cmd)
            print cmd
    
    #ALIGN
    if opts.step_to_perform=='align':
        alignment_script=opts.code_path+'new_ase_code/ase/bin/alignBatch.sh'
        for sample_name in sample_di.keys():
            if sample_name not in of_interest:
                continue
            if sample_di[sample_name]['alignment_directory']=='NA':
                sys.exit('No alignment directory provided for '+sample_name+'. Exiting ..')
            alignment_prefix=sample_di[sample_name]['alignment_directory']+sample_di[sample_name]['sample_name']
            #Make sure genome exists
            if os.path.isfile(sample_di[sample_name]['genome_path']+'/'+sample_di[sample_name]['individual'].split('-')[0]+'.maternal.bwt'):
                #First, make the file required for alignBatch.sh
                info_file=sample_di[sample_name]['alignment_directory']+'info_'+sample_di[sample_name]['sample_name']
                make_info='echo '+sample_di[sample_name]['sample_name']+' '+sample_di[sample_name]['individual'].split('-')[0]+' '+os.path.basename(sample_di[sample_name]['fastq1'])+' '+os.path.basename(sample_di[sample_name]['fastq2'])+' > '+info_file
                os.system(make_info)
                #Run alignment
                cmd=alignment_script+' -f '+os.path.dirname(sample_di[sample_name]['fastq1'])+' -b '+sample_di[sample_name]['alignment_directory']+' -s '+sample_di[sample_name]['genome_path']+' -l '+info_file
                print cmd
                os.system(cmd)
                #print cmd

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
