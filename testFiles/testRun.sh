
#INSTALLATION ==========================
CODEDIR=/srv/gsfs0/projects/kundaje/users/oursu/code/git_things/Personal_genome_mapping
#Setup ase code
#Load modules boost and cmake
#For scg3 uncomment the following 2 lines
#module add boost/1.51.0
#module add cmake/2.8.11.2
cd ${CODEDIR}/new_ase_code/ase_cpp
chmod 711 configure.sh 
./configure.sh
make
#Now you have just installed the ase code. Congratulations!
#========================================


#TEST FILES ======================================================================================
#Here are some test files to check that personal genome mapping works correctly.
#We will work with NA19099, vcf from 1000Genomes, and a small fasta file of 1M reads, PE.
#H3K27AC Rep1 from "Extensive variation in chromatin states"
CODEDIR=/srv/gsfs0/projects/kundaje/users/oursu/code/git_things/Personal_genome_mapping
TESTDIR=${CODEDIR}/testFiles

vcf=${TESTDIR}/NA19099.vcf
fq1=${TESTDIR}/NA19099.H3K27AChead100.FQ1.fastq.gz
fq2=${TESTDIR}/NA19099.H3K27AChead100.FQ2.fastq.gz
metadata=${TESTDIR}/metadata
echo "test" | awk '{print "#IndividualSampleName\tFQ1\tFQ2\tGenomePath\tGender\tVcfFile\tAlignmentDirectory"}' > ${metadata}
echo "test" | awk -v afq1=$fq1 -v afq2=$fq2 -v gpath=$TESTDIR -v avcf=$vcf -v aligndir=$TESTDIR/ '{print "NA19099\tNA19099_H3K27AC_25reads\t"afq1"\t"afq2"\t"gpath"\tfemale\t"avcf"\t"aligndir}' >> ${metadata}

#scg3 specific but you can set your own
#directory with fasta files, one per chromosome
fadir=/srv/gs1/projects/kundaje/oursu/Alignment/data/ENCODE_genomes/male/
genomedict=/srv/gs1/projects/kundaje/oursu/Alignment/data/ENCODE_genomes/male/ref.fa.fai

#1. Let's make a personal genome!
python ${CODEDIR}/MAPPING_wrapper.py --bashrc_file ${CODEDIR}/personal_genome_mapping.bashrc --code_path ${CODEDIR}/ --metadata ${metadata} --step_to_perform createGenome --fadir_male ${fadir} --genome_dict_male ${genomedict} --BWAindex --BowtieIndex --chromo

#2. ========= RNA mapping =========
#Align with Tophat to the personal genome (indexed in the previous step)
python ${CODEDIR}/MAPPING_wrapper.py --bashrc_file ${CODEDIR}/personal_genome_mapping.bashrc --code_path ${CODEDIR}/ --metadata ${metadata} --fadir_male ${fadir} --genome_dict_male ${genomedict} --step_to_perform alignTopHat
#Reconcile the reads
python ${CODEDIR}/MAPPING_wrapper.py --bashrc_file ${CODEDIR}/personal_genome_mapping.bashrc --code_path ${CODEDIR}/ --metadata ${metadata} --fadir_male ${fadir} --genome_dict_male ${genomedict} --step_to_perform reconcileTopHat

#3. ======== DNA mapping =========
#Align reads with BWA


