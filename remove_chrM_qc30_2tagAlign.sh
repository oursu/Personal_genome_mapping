#!/bin/bash
usage()
{
cat <<EOF
usage: `basename $0` options
Filters out 1) reads not properly paired, 2) unmapped reads and their mates, 3) reads on the M chromosome. Then it converts to the end tagAlign format.
OPTIONS:
   -h           Show this message and exit
   --indir DIR  [Required] Input directory.
   --outdir DIR [Required] Output directory.
   --sample STR [Required] Sample name. Input files are read from <indir>/<sample>.bam and output is written in <outdir>/<sample>.tagAlign.bed.gzip.
EOF
}

ARGS=`getopt -o "hcns" -l "indir:,outdir:,sample:" -- "$@"`
eval set -- "$ARGS"

INDIR=
OUTDIR=
SAMPLE=
READS=
while [ $# -gt 0 ]; do
    case $1 in
    -h) usage; exit;;
    --indir) INDIR=$2; shift 2;;
    --outdir) OUTDIR=$2; shift 2;;
    --sample) SAMPLE=$2; shift 2;;
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

script_location=${OUTDIR}/${SAMPLE}_remove_chrM_qc30_2tagAlign_script.sh
inpref=${INDIR}/${SAMPLE}
outpref=${OUTDIR}/${SAMPLE}.q30.nochrM
mkdir ${OUTDIR}
SAMTOOLS_PATH=/srv/gs1/software/samtools/samtools-0.1.19/bin/samtools

module add bedtools/2.18.0
${SAMTOOLS_PATH} view -f3 -q30 -F1548 -h ${inpref}.bam | grep -v chrM | awk '$4 !="*"{print $0}' | ${SAMTOOLS_PATH} view -S -b - | ${SAMTOOLS_PATH} sort -m 2000000000 - ${outpref}
${SAMTOOLS_PATH} index ${outpref}.bam
bamToBed -i ${outpref}.bam | awk 'BEGIN{FS="\t";OFS="\t"}{$5="1000" ; print $0}' | gzip > ${outpref}.tagAlign.gz
#qsub -l h_vmem=3G -o ${script_location}.o -e ${script_location}.e ${script_location} 
