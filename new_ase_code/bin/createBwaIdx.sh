#!/bin/bash

usage()
{
cat <<EOF
usage: `basename $0` options
Create BWA or Bowtie index for paternal and maternal versions of several genomes.
OPTIONS:
   -h     Show this message and exit
   -i DIR [Required] Input directory.
   -o DIR Output directory [default: input directory].
   -x STR Type of index (bwa or bowtie2) [default: bwa].
   -e RE  Regular expression. Index of <RE>.*[mp]aternal.fa will be created [default: .*].
EOF
}

echo "here"
INDIR=
OUTDIR=
IDX='bwa'
EXPR='.*'
while getopts "hi:o:x:e:" opt
do
    case $opt in
	h)
	    usage; exit;;
	i)
	    INDIR=$OPTARG;;
	o)
	    OUTDIR=$OPTARG;;
	x)
	    IDX=$OPTARG;;
	e) 
	    EXPR=$OPTARG;;
	?)
	    usage
	    exit 1;;
    esac	    
done
if [[ -z $INDIR ]]; then
    usage; exit 1;
fi
if [[ -z $OUTDIR ]]; then
    OUTDIR=$INDIR
fi
if [ ! -d $OUTDIR ]; then
    mkdir -p $OUTDIR
fi
if [ ! -d $INDIR ]; then
    echo 'Indir does not exist' 1>&2; exit 1;
fi


BWA_PATH=/srv/gs1/software/bwa/bwa-0.6.1/bin/bwa
echo $BWA_PATH
FILES="${EXPR}.*[mp]aternal.fa$"
echo ${INDIR}
echo ${OUTDIR}
for file in `ls ${INDIR} | egrep "$FILES"`; do
    pref=${file%.fa}
    echo $pref
    if [[ $IDX =~ "bwa" ]]; then
	echo "bwa"
	module load bwa/0.7.7
	bwa index -a bwtsw -p ${OUTDIR}/${pref} ${INDIR}/${file}
	#echo "${BWA_PATH} index -a bwtsw -p ${OUTDIR}/${pref} ${INDIR}/${file}" > ${OUTDIR}/scripts/${pref}_bwaIndex_call.sh
	echo "wrote script"
	chmod 711 ${OUTDIR}/scripts/${pref}_bwaIndex_call.sh
	#qsub -l mem_free=50G -l h_vmem=50G -l h_rt=20:00:00 -o ${OUTDIR}/scripts/${pref}_bwaIndex_call.o -e ${OUTDIR}/scripts/${pref}_bwaIndex_call.e ${OUTDIR}/scripts/${pref}_bwaIndex_call.sh
	${OUTDIR}/scripts/${pref}_bwaIndex_call.sh
	#bsub -J ${pref} -e ${OUTDIR}/${pref}.idx.err -o /dev/null -q research-rh6 -M 8192 -R "rusage[mem=8192]" "bwa index -a bwtsw -p ${OUTDIR}/${pref} ${INDIR}/${file}"
    elif [[ $IDX =~ bow.*2 ]]; then
	echo "bow2"
	#TODO: make this work
	#echo bowtie2-build -f ${INDIR}/$file ${OUTDIR}/${pref} > ${OUTDIR}/scripts/${pref}_bowtie2Index_call.sh
	#chmod 711 ${OUTDIR}/scripts/${pref}_bowtie2Index_call.sh
	#qsub -l mem_free=20G -l h_vmem=20G -l h_rt=20:00:00 -o ${OUTDIR}/scripts/${pref}_bowtie2Index_call.o -e ${OUTDIR}/scripts/${pref}_bowtie2Index_call.e ${OUTDIR}/scripts/${pref}_bowtie2Index_call.sh
	#bsub -J ${pref} -e ${OUTDIR}/${pref}.idx.bow2.err -o /dev/null -q research-rh6 -M 8192 -R "rusage[mem=8192]" "bowtie2-build -f ${INDIR}/$file ${OUTDIR}/${pref}"
    fi
done