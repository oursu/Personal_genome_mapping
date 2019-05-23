#!/bin/bash

usage()
{
cat <<EOF
usage: `basename $0` options
Reconciles a maternal and a paternal bam into one file.
OPTIONS:
   -h           Show this message and exit
   --indir DIR  [Required] Input directory.
   --outdir DIR [Required] Output directory.
   --sample STR [Required] Sample name. Input files are read from <indir>/<sample>_[mp]aternal.bam and output is written in <outdir>/<sample>_reconcile.bam.
   --sfile  STR Source file
   -n           Also sort deduped output by read name [0].
   -s           Single end reads.
   -c           Overwrite output files [0]
EOF
}

ARGS=`getopt -o "hcns" -l "indir:,outdir:,sample:,sfile:" -- "$@"`
eval set -- "$ARGS"

CLEAN=0
NSORT=0
PAIRED=1
INDIR=
OUTDIR=
SAMPLE=
SFILE=
while [ $# -gt 0 ]; do
    case $1 in
	-h) usage; exit;;
	--indir) INDIR=$2; shift 2;;
	--outdir) OUTDIR=$2; shift 2;;
	--sample) SAMPLE=$2; shift 2;;
	--sfile) SFILE=$2; shift 2;;
	-n) NSORT=1; shift;;
	-c) CLEAN=1; shift;;
	-s) PAIRED=0; shift;;
	--) shift; break;;
	*) usage; exit 1;;
    esac	    
done

if [ $# -ne 0 ]; then
    usage; exit 1;
fi

if [[ -z $INDIR || -z $OUTDIR || -z $SAMPLE ]]; then
    usage; exit 1;
fi

if [ ! -d ${OUTDIR}/dedup/q30 ]; then
    mkdir -p ${OUTDIR}/dedup/q30
fi
if [[ $NSORT -eq 1 ]]; then
    mkdir -p ${OUTDIR}/dedup/nsort
fi

tmpdir=${OUTDIR}/${SAMPLE}_tmp
if [ -d $tmpdir ]; then
    echo "Existing temporary directory! Aborting..." 1>&2; exit 1;
else
    mkdir ${tmpdir}
fi
tmppref=${tmpdir}/tmp
inpref=${INDIR}/${SAMPLE}
outpref=${OUTDIR}/${SAMPLE}_reconcile
dedpref=${OUTDIR}/dedup/${SAMPLE}_reconcile.dedup
qpref=${OUTDIR}/dedup/q30/${SAMPLE}_reconcile.dedup
npref=${OUTDIR}/dedup/nsort/${SAMPLE}_reconcile.dedup
source ${SFILE}

if [[ ( ! -s ${inpref}_maternal.bam ) || ( ! -s ${inpref}_paternal.bam ) ]]; then
    echo "Skipping $SAMPLE. Maternal and/or paternal bam file missing." 1>&2; exit 1;
fi

if [[ $CLEAN -eq 1 || ! -f ${outpref}.bam ]]; then
    ${CODEDIR}/new_ase_code/ase_cpp/bin/Ase reconcile rg1=paternal rg2=maternal $PAIRED ${inpref}_paternal.bam ${inpref}_maternal.bam ${tmppref}.bam > ${outpref}.out
    #${ASE_CODE} reconcile rg1=paternal rg2=maternal $PAIRED ${inpref}_paternal.bam ${inpref}_maternal.bam ${tmppref}.bam > ${outpref}.out
    num=`samtools view ${tmppref}.bam | head -1 | egrep "_[12]:N:0:[ACGT]+" | wc -l`
    if [[ $num -gt 0 ]]; then
	samtools view -h ${tmppref}.bam | sed -r 's/_[12]:N:0:[ACGT]+//' | samtools view -Sb - | samtools sort -m 2000000000 -o ${outpref}.bam -
    else
	samtools sort -m 2000000000 -o ${outpref}.bam ${tmppref}.bam
    fi
    samtools index ${outpref}.bam
fi

if [[ $CLEAN -eq 1 || ! -f ${dedpref}.bam ]]; then
    echo "Removing duplicates..." 1>&2;
    #${MARKDUPLICATESCMD}  I=${outpref}.bam O=${dedpref}.bam M=${dedpref}.stats AS=true TMP_DIR=${tmpdir} VALIDATION_STRINGENCY=LENIENT MAX_RECORDS_IN_RAM=1000000 REMOVE_DUPLICATES=true
    #/usr/java/latest/bin/java -Xmx2G -jar /home/oursu/devtools/picard-tools-1.105/MarkDuplicates.jar I=${outpref}.bam O=${dedpref}.bam M=${dedpref}.stats AS=true TMP_DIR=${tmpdir} VALIDATION_STRINGENCY=LENIENT MAX_RECORDS_IN_RAM=1000000 REMOVE_DUPLICATES=true
    #samtools index ${dedpref}.bam
fi

#
#if [[ $CLEAN -eq 1 || ! -f ${qpref}.bam ]]; then
#    echo 'decided to do q30 filtering'
#    ${SAMTOOLS_PATH} view -q 30 -bh ${dedpref}.bam > ${qpref}.bam 
#    ${SAMTOOLS_PATH} index ${qpref}.bam
#    for g in maternal paternal; do
#	${SAMTOOLS_PATH} view -q 30 -r $g -bh ${dedpref}.bam > ${qpref}.${g}.bam 
#	${SAMTOOLS_PATH} index ${qpref}.${g}.bam
#    done
#fi

if [[ $NSORT -eq 1 && ( $CLEAN -eq 1 || ! -f ${npref}.bam ) ]]; then
    samtools sort -n -m 2000000000 ${dedpref}.bam $npref
fi

if [ -d $tmpdir ]; then
    rm -r $tmpdir
fi
