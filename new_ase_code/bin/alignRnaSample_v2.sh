#!/bin/bash

usage()
{
cat <<EOF
usage: `basename $0` options
Aligns an RNA sample with TopHat
OPTIONS:
   -h            Show this message and exit
   --fq1 FILE    [Required]
   --fq2 FILE    [Required] Fastq files. Say NA fpr SE analysis.
   --bamdir DIR  [Required] Dir where bam files will be written
   --mpref STR   [Required] Prefix of name sorted file.
   --seqpref STR [Required] Prefix for genome index files
   --trpref STR  [Required] Prefix for transcriptome index files (will be created if they don't exist) 
   --gtf FILE    [Required] GTF file with known transcriptome.                                         
   --source_file [Required] Source file   
   -c            Overwrite output files [0]
   -j            Set this if you want novel junctions. Otherwise, tophat will be run with --no-novel-juncs
EOF
}

ARGS=`getopt -o "hc" -l "fq1:,fq2:,bamdir:,seqpref:,trpref:,mpref:,gtf:,sfile:" -- "$@"`
eval set -- "$ARGS"

CLEAN=0
NOVELJUNCS=0
BAMDIR=
FQ1=
FQ2=
SEQPREF=
TRPREF=
MPREF=
GTF=
SFILE=
while [ $# -gt 0 ]; do
    case $1 in
	-h) usage; exit;;
	--fq1) FQ1=$2; shift 2;;
	--fq2) FQ2=$2; shift 2;;
	--bamdir) BAMDIR=$2; shift 2;;
	--seqpref) SEQPREF=$2; shift 2;;
	--mpref) MPREF=$2; shift 2;;
	--trpref) TRPREF=$2; shift 2;;
	--gtf) GTF=$2; shift 2;;
	--sfile) SFILE=$2;shift 2;;
	-c) CLEAN=1; shift;;
	-j) NOVELJUNCS=1; shift;;
	--) shift; break;;
    esac	    
done

if [ $# -ne 0 ]; then
    usage; exit 1;
fi

if [[ -z $BAMDIR || -z $FQ1 || -z $FQ2 || -z $SEQPREF || -z $TRPREF || -z $MPREF || -z $GTF || -z $SFILE ]]; then
    usage; exit 1;
fi

if [ ! -d $BAMDIR ]; then
    mkdir -p $BAMDIR
fi

alignScript=${BAMDIR}/${MPREF}_script.sh

source ${SFILE}
echo "source ${SFILE}" > ${alignScript}
# TopHat options
ALN="-p 4 --no-discordant --library-type fr-firststrand --b2-sensitive --no-novel-indels --no-novel-juncs"
if [[ $NOVELJUNCS -eq 1 ]]; then
    ALN="-p 4 --no-discordant --library-type fr-firststrand --b2-sensitive --no-novel-indels"
fi

echo "Alignment parameters:"
echo $ALN

#PE analysis unless FQ2=="NA"
if [[ -s ${FQ1} ]]; then
    # Check Illumina version 
    format=`${python276} ${CODEDIR}/new_ase_code/python/checkFastq_2014-03-03.py --fastq $FQ1`
    echo ${format}
    if [[ $format == 'Solexa' ]]; then
	ALN="$ALN --solexa1.3-quals"
    fi

    #decide whether we are using a GTF file or not
    if [[ ${GTF} != "NA" ]]; then
	if [[ -f ${TRPREF}.gff ]]; then
	    if [[ ! -f ${TRPREF}.1.bt2 ]]; then
	        # TopHat will break if the gff is there but the index is not
		rm ${TRPREF}.gff
		ALN="$ALN --GTF $GTF"
	    fi
	else
	    ALN="$ALN --GTF $GTF"
	fi
    fi
    if [[ $CLEAN -eq 1 || ! -f ${BAMDIR}/accepted_hits.bam ]]; then
	if [[ ${GTF} != "NA" ]]; then
	    if [[ $FQ2 == "NA" ]]; then #SE analysis
		echo "tophat2 $ALN -o $BAMDIR/${MPREF} --transcriptome-index $TRPREF $SEQPREF ${FQ1}" >> ${alignScript}
	    else
		echo "tophat2 $ALN -o $BAMDIR/${MPREF} -r 200 --mate-std-dev 20 --transcriptome-index $TRPREF $SEQPREF ${FQ1} ${FQ2}" >>${alignScript} 
	    fi
	else
	    #no gtf file here
	    if [[ $FQ2 == "NA" ]]; then #SE analysis
		echo "tophat2 $ALN -o $BAMDIR/${MPREF} $SEQPREF ${FQ1}" >>${alignScript} 
	    else
		echo "tophat2 $ALN -o $BAMDIR/${MPREF} -r 200 --mate-std-dev 20 $SEQPREF ${FQ1} ${FQ2}" >>${alignScript}
	    fi
	fi
    fi

    if [[ $CLEAN -eq 1 || ! -f ${BAMDIR}/${MPREF}.bam ]]; then
	echo "samtools view -H ${BAMDIR}/${MPREF}/accepted_hits.bam | sed 's/SO:coordinate/SO:unsorted/' > ${BAMDIR}/${MPREF}/header.sam" >>${alignScript}
	echo "samtools cat -h ${BAMDIR}/${MPREF}/header.sam ${BAMDIR}/${MPREF}/accepted_hits.bam ${BAMDIR}/${MPREF}/unmapped.bam | samtools view -b -F0x100 - | samtools sort -n -m 2000000000 - ${BAMDIR}/${MPREF}" >>${alignScript}
	echo "rm ${BAMDIR}/${MPREF}/accepted_hits.bam ${BAMDIR}/${MPREF}/*bed ${BAMDIR}/${MPREF}/unmapped.bam" >> ${alignScript}
	#echo "rm -r ${BAMDIR}/${MPREF}" >> ${alignScript}
    fi
fi

echo "here is the script"
more ${alignScript}
chmod 711 ${alignScript}
${alignScript}

