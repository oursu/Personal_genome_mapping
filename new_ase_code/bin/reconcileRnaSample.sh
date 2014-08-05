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
   --sample STR [Required] Sample name. Input files are read from <indir>/<sample>_[mp]aternal and output is written in <outdir>/<sample>_reconcile.bam.
   --source_file [Required] Source file  
   --paired     [Required] set to 1 if paired end reads
   -c           Overwrite output files [0]
EOF
}

ARGS=`getopt -o "hc" -l "indir:,outdir:,sample:,sfile:,paired:" -- "$@"`
eval set -- "$ARGS"

PAIRED=0
CLEAN=0
INDIR=
OUTDIR=
SAMPLE=
while [ $# -gt 0 ]; do
    case $1 in
	-h) usage; exit;;
	--indir) INDIR=$2; shift 2;;
	--outdir) OUTDIR=$2; shift 2;;
	--sample) SAMPLE=$2; shift 2;;
	--paired) PAIRED=$2; shift 2;;
	--sfile) SFILE=$2;shift 2;;
	-c) CLEAN=1; shift;;
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

if [ ! -d ${OUTDIR}/reconcile/dedup ]; then
    mkdir -p ${OUTDIR}/reconcile/dedup
fi

tmpdir="${OUTDIR}/tmp_${SAMPLE}_${RANDOM}"
if [ -d $tmpdir ]; then
    echo "Existing temporary directory! Aborting..." 1>&2; exit 1;
else
    mkdir $tmpdir
fi

source ${SFILE}
tmppref=${tmpdir}/tmp
inpref=${INDIR}/${SAMPLE}
outpref=${OUTDIR}/${SAMPLE}
recpref=${OUTDIR}/reconcile/${SAMPLE}_reconcile
dedpref=${OUTDIR}/reconcile/dedup/${SAMPLE}_reconcile.dedup

reconcileScript=${dedpref}_script.sh
echo "source ${SFILE}" > ${reconcileScript}

if [[ ( ! -s ${inpref}_maternal.bam ) || ( ! -s ${inpref}_paternal.bam ) ]]; then
    echo "Skipping $SAMPLE. Maternal and/or paternal bam file missing." 1>&2; exit 1;
fi

if [[ $CLEAN -eq 1 || ! -f ${recpref}.bam ]]; then
    #First, need to make sure both maternal and paternal alignments have the same reads. They should, but sometimes they don't.
    #echo "samtools view ${inpref}_paternal.bam | cut -f1 > ${inpref}_paternal.bam_reads" >> ${reconcileScript}
    #echo "samtools view ${inpref}_maternal.bam | cut -f1 > ${inpref}_maternal.bam_reads" >> ${reconcileScript}
    #echo "comm -3 ${inpref}_paternal.bam_reads ${inpref}_maternal.bam_reads > ${inpref}_NOTshared_reads" >> ${reconcileScript}
    #echo "samtools view ${inpref}_paternal.bam | grep -v -f ${inpref}_NOTshared_reads | samtools view -bhS - > ${inpref}_paternal.sharedReads.bam" >> ${reconcileScript}
    #echo "samtools view ${inpref}_maternal.bam | grep -v -f ${inpref}_NOTshared_reads | samtools view -bhS - > ${inpref}_maternal.sharedReads.bam" >> ${reconcileScript}
    echo '${CODEDIR}'"/new_ase_code/ase_cpp/bin/Ase reconcile rg1=paternal rg2=maternal ${PAIRED} ${inpref}_paternal.bam ${inpref}_maternal.bam ${tmppref}.bam > ${recpref}.out" >> ${reconcileScript}
    echo "samtools sort -m 2000000000 ${tmppref}.bam ${recpref}" >> ${reconcileScript}
    echo "samtools index ${recpref}.bam" >> ${reconcileScript}
fi

if [[ $CLEAN -eq 1 || ! -f ${dedpref}.bam ]]; then
    echo '${MARKDUPLICATESCMD}'" I=${recpref}.bam O=${dedpref}.bam M=${dedpref}.stats AS=true TMP_DIR=${tmpdir} VALIDATION_STRINGENCY=LENIENT MAX_RECORDS_IN_RAM=1000000 REMOVE_DUPLICATES=true" >> ${reconcileScript}
    echo "samtools index ${dedpref}.bam" >> ${reconcileScript}
    echo "rm -r ${tmpdir}" >> ${reconcileScript}
fi

chmod 711 ${reconcileScript}
${reconcileScript}
