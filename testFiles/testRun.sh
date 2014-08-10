
#INSTALLATION ==========================
#### USER MUST CHANGE: Change CODEDIR below to be the directory where you have cloned the code.
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
#We will work with NA19099, vcf from 1000Genomes, and a small fasta file of 250 reads, PE.
#H3K27AC Rep1 from "Extensive variation in chromatin states"
CODEDIR=/srv/gsfs0/projects/kundaje/users/oursu/code/git_things/Personal_genome_mapping
TESTDIR=${CODEDIR}/testFiles
datadir=${TESTDIR}/data

vcf=${datadir}/NA19099.vcf
fq1=${datadir}/NA19099.H3K27AChead1000.FQ1.fastq.gz
fq2=${datadir}/NA19099.H3K27AChead1000.FQ2.fastq.gz
metadata=${TESTDIR}/metadata
tophatdir=$TESTDIR/Tophat_alignments/
bwadir=$TESTDIR/BWA_alignments/
genomedir=$TESTDIR/genome
mkdir ${tophatdir}
mkdir ${bwadir}
mkdir ${genomedir}
echo "test" | awk '{print "#IndividualSampleName\tFQ1\tFQ2\tGenomePath\tGender\tVcfFile\tAlignmentDirectory"}' > ${metadata}.forTophat
echo "test" | awk '{print "#IndividualSampleName\tFQ1\tFQ2\tGenomePath\tGender\tVcfFile\tAlignmentDirectory"}' > ${metadata}.forBWA
echo "test" | awk -v afq1=$fq1 -v afq2=$fq2 -v gpath=${genomedir} -v avcf=$vcf -v aligndir=${tophatdir} '{print "NA19099\tNA19099_H3K27AC_250reads\t"afq1"\t"afq2"\t"gpath"\tfemale\t"avcf"\t"aligndir}' >> ${metadata}.forTophat
echo "test" | awk -v afq1=$fq1 -v afq2=$fq2 -v gpath=${genomedir} -v avcf=$vcf -v aligndir=${bwadir} '{print "NA19099\tNA19099_H3K27AC_250reads\t"afq1"\t"afq2"\t"gpath"\tfemale\t"avcf"\t"aligndir}' >> ${metadata}.forBWA

#scg3 specific but you can set your own.
#directory with fasta files, one per chromosome
fadir=/srv/gs1/projects/kundaje/oursu/Alignment/data/ENCODE_genomes/male/
#A file with chr, and chr size as the first 2 columns
genomedict=/srv/gs1/projects/kundaje/oursu/Alignment/data/ENCODE_genomes/male/ref.fa.fai


#---------------------------------------------------------------------
#--------------------------- TEST RUN --------------------------------
#---------------------------------------------------------------------
#1. ======== Personal genome construction ========
python ${CODEDIR}/MAPPING_wrapper.py --bashrc_file ${CODEDIR}/personal_genome_mapping.bashrc --code_path ${CODEDIR}/ --metadata ${metadata}.forTophat --step_to_perform createGenome --fadir_male ${fadir} --genome_dict_male ${genomedict} --BWAindex --BowtieIndex --chromo







#2. ========= RNA mapping =========
#Align with Tophat to the personal genome (indexed in the previous step).
#If you want to provide a gtf file (to align to the personal transcriptome), or for other such options, you can run the command below, to see which settings you can change
#python ${CODEDIR}/MAPPING_wrapper.py -h
python ${CODEDIR}/MAPPING_wrapper.py --bashrc_file ${CODEDIR}/personal_genome_mapping.bashrc --code_path ${CODEDIR}/ --metadata ${metadata} --fadir_male ${fadir} --genome_dict_male ${genomedict} --step_to_perform alignTopHat
#Reconcile the reads
python ${CODEDIR}/MAPPING_wrapper.py --bashrc_file ${CODEDIR}/personal_genome_mapping.bashrc --code_path ${CODEDIR}/ --metadata ${metadata} --fadir_male ${fadir} --genome_dict_male ${genomedict} --step_to_perform reconcileTopHat

#3. ======== DNA mapping =========
#Align reads with BWA to the personal genome
python ${CODEDIR}/MAPPING_wrapper.py --bashrc_file ${CODEDIR}/personal_genome_mapping.bashrc --code_path ${CODEDIR}/ --metadata ${metadata} --fadir_male ${fadir} --genome_dict_male ${genomedict} --step_to_perform alignBWA

