#!/bin/bash

usage()
{
cat <<EOF
usage: `basename $0` options
Runs BWA on a single sample
OPTIONS:
   -h            Show this message and exit
   --fq1 FILE    [Required]
   --fq2 FILE    [Required] Fastq files
   --bamdir DIR  [Required] Dir where bam files will be written
   --seqpref STR [Required] Prefix for BWA genome index files
   --sample STR  [Required] Sample name. Output will be in <bamdir>/<sample>.bam.
   -c            Overwrite output files [0]
   -p            Sort by position (by default sorts by read name).
EOF
}

ARGS=`getopt -o "hcp" -l "fq1:,fq2:,bamdir:,seqpref:,sample:" -- "$@"`
eval set -- "$ARGS"

CLEAN=0
BAMDIR=
FQ1=
FQ2=
SEQPREF=
SAMPLE=
SORTPOS=0
while [ $# -gt 0 ]; do
    case $1 in
	-h) usage; exit;;
	--fq1) FQ1=$2; shift 2;;
	--fq2) FQ2=$2; shift 2;;
	--bamdir) BAMDIR=$2; shift 2;;
	--seqpref) SEQPREF=$2; shift 2;;
	--sample) SAMPLE=$2; shift 2;;
	-c) CLEAN=1; shift;;
	-p) SORTPOS=1; shift;;
	--) shift; break;;
    esac	    
done

if [ $# -ne 0 ]; then
    usage; exit 1;
fi

if [[ -z $BAMDIR || -z $FQ1 || -z $FQ2 || -z $SEQPREF || -z $SAMPLE ]]; then
    usage; exit 1;
fi

#if [-z $LOGDIR ]
#then
#    LOGDIR=${BAMDIR}/bwaLog
#fi
if [ ! -d $BAMDIR ]; then
    mkdir -p $BAMDIR
fi

# -I not needed if you do SeqPrep first!
# DOUBLE-CHECK THESE PARAMETERS
#Oana: changed these parameters to the ENCODE guidelines ALN="-q 20 -t 4"
#what i want: ALN="-q 15 -l 32 -k 2"
ALN="-q 20 -t 4"
if [[ $SORTPOS -eq 1 ]]; then
    SORTOPT=""
else
    SORTOPT="-n"
fi

#### BWA ####
BWA_PATH=/srv/gs1/software/bwa/bwa-0.6.1/bin/bwa
SAMTOOLS_PATH=/srv/gs1/software/samtools/samtools-0.1.19/bin/samtools
CODE_DIR=/srv/gsfs0/projects/kundaje/users/oursu/code/personalGenomeAlignment/new_ase_code/ase
if [[ -s ${FQ1} && ( -s ${FQ2} || $FQ2 == "NA" ) ]]; then
    # Check Illumina version
    format=`/home/oursu/devtools/Python-2.7.6/python /srv/gsfs0/projects/kundaje/users/oursu/code/personalGenomeAlignment/new_ase_code/ase/python/checkFastq_2014-03-03.py --fastq $FQ1`
    echo ${format}
    if [[ $format == 'Illumina_1_3' ]]; then
	ALN="$ALN -I"
    fi
    
    if [[ $CLEAN -eq 1 || ! -f ${BAMDIR}/${SAMPLE}_1.sai ]]; then
	${BWA_PATH} aln $ALN $SEQPREF ${FQ1} -f ${BAMDIR}/${SAMPLE}_1.sai #2>> ${logfile}
    fi
    if [[ $FQ2 != "NA" && ( $CLEAN -eq 1 || ! -f ${BAMDIR}/${SAMPLE}_2.sai ) ]]; then
	${BWA_PATH} aln $ALN $SEQPREF ${FQ2} -f ${BAMDIR}/${SAMPLE}_2.sai #2>> ${logfile}
    fi
else
    echo "Missing or empty FASTQ files. Aborting..." 1>&2 ; exit 1;
fi
    
if [[ -s ${BAMDIR}/${SAMPLE}_1.sai && ( $FQ2 == "NA" || -s ${BAMDIR}/${SAMPLE}_2.sai ) ]]; then
    if [[ $CLEAN -eq 1 || ! -f ${BAMDIR}/${SAMPLE}.bam ]]; then
	head="@RG\tID:${SAMPLE}\tSM:${SAMPLE}\tPL:Illumina"
	if [[ $FQ2 == "NA" ]]; then
	    ${BWA_PATH} samse -r $head $SEQPREF ${BAMDIR}/${SAMPLE}_1.sai ${FQ1} | sed -r 's/_[12]:N:0:[ACGT]+//' | ${SAMTOOLS_PATH} view -Sbh -t ${SEQPREF}.fa.fai - | ${SAMTOOLS_PATH} sort $SORTOPT -m 2000000000 - ${BAMDIR}/${SAMPLE}
	else
            # Notice the sort by name here...
	    ${BWA_PATH} sampe -r $head $SEQPREF ${BAMDIR}/${SAMPLE}_1.sai ${BAMDIR}/${SAMPLE}_2.sai ${FQ1} ${FQ2} | sed -r 's/_[12]:N:0:[ACGT]+//' | ${SAMTOOLS_PATH} view -Sbh -t ${SEQPREF}.fa.fai - | ${SAMTOOLS_PATH} sort $SORTOPT -m 2000000000 - ${BAMDIR}/${SAMPLE}
	fi
	if [[ $SORTPOS -eq 1 ]]; then
	    ${SAMTOOLS_PATH} index ${BAMDIR}/${SAMPLE}.bam
	fi
    fi
else
    echo ".sai files missing. Aborting..." 1>&2 ; exit 1;
fi
