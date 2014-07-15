#!/bin/bash

usage()
{
cat <<EOF
EOF                                                                                                                                                                    
usage: `basename $0` options                                                                                                                                               
Removes duplicate reads and filters reads by q30                                                                                                                         
    
OPTIONS:                                                                                                                                                                    
   -h           Show this message and exit                                                                                                                                 
   --indir DIR  [Required] Input directory.                                                                                                                                
   --outdir DIR [Required] Output directory.                                                                                                                             
   --sample STR [Required] Sample name. Input files are read from <indir>/<sample>.bam and output is written in <outdir>/<sample>.properPairs.Mapped.nochrM.tagAlign.bed
EOF
}

ARGS=`getopt -o "hcns" -l "indir:,outdir:,sample:" -- "$@"`
eval set -- "$ARGS"

INDIR=
OUTDIR=
SAMPLE=
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

operationName=properPairs.Mapped.nochrM.tagAlign.bed
script_location=${OUTDIR}/${SAMPLE}_${operationName}.sh
inpref=${INDIR}/${SAMPLE}
SAMTOOLS_PATH=/srv/gs1/software/samtools/samtools-0.1.19/bin/samtools

#FILTER BAM (keep proper pairs and remove unmapped)
echo ${SAMTOOLS_PATH}' view -f3 -F4 -bh -s 0.01 '${inpref}'.bam  > '${inpref}'_f3_F4.bam' > ${script_location}
echo ${SAMTOOLS_PATH}' view -F8 -bh '${inpref}'_f3_F4.bam > '${inpref}'properPairs.Mapped.bam' >> ${script_location}

#REMOVE CHRM

#SUBSAMPLE BAM

#MAKE A BED

#All in one
echo '${SAMTOOLS_PATH} view -f3 -F4 -bh -s 0.01 ${inpref}.bam | ${SAMTOOLS_PATH} view -h -F8 - | grep -vw chrM | ${SAMTOOLS_PATH} view -Sb -h - |  bamToBed -i stdin | > ${inpref}${operationName}' > ${script_location} 

#subsampling should happen later
echo "${SAMTOOLS_PATH} view ${inpref}properPairs.Mapped.bam | grep -vw chrM | awk ' 
'${SAMTOOLS_PATH}' view -Sb > '${inpref}${operationName} |  >> ${script_location}


#subsample just the bam
#make just a bam, no beds
