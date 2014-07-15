#!/bin/bash
usage()
{
cat <<EOF
usage: `basename $0` options
OPTIONS:
   -h           Show this message and exit
   --vcf1 File  vcf1
   --vcf2 File  vcf2
   --out1  Dir   Directory where to output results
   --chromo chromo
EOF
}

ARGS=`getopt -o "hcns" -l "vcf1:,vcf2:,out1:,chromo:" -- "$@"`
eval set -- "$ARGS"

while [ $# -gt 0 ]; do
    case $1 in
    -h) usage; exit;;
    --vcf1) VCF1=$2; shift 2;;
    --vcf2) VCF2=$2; shift 2;;
    --out1) OUT=$2; shift 2;;
    --chromo) CHROMO=$2; shift 2;;
    --) shift; break;;
    *) usage; exit 1;;
    esac          
done

echo ${VCF1}
echo ${VCF2}
echo ${OUT}
chromo=${CHROMO}
mkdir ${OUT}

script=${OUT}/chr${chromo}_script.sh
VCF1_info=${OUT}/$(basename ${VCF1})SNPinfo_chr${chromo}
VCF2_info=${OUT}/$(basename ${VCF2})SNPinfo${chromo}
#Get SNPs that are found in both 
#Get SNP information only. Label SNPs for which information does not agree
VCFcompare=${OUT}/COMPARE_$(basename ${VCF1})_VS_$(basename ${VCF2})
echo "cat ${VCF1} | awk '\$1==${chromo} { print \$1\"_\"\$2\"_\"\$3\"\t\"\$1\"\t\"\$2\"\t\"\$3\"\t\"\$4\"\t\"\$5}' | sort > ${VCF1_info}" > ${script}
echo "cat ${VCF2} | awk '\$1==${chromo} { print \$1\"_\"\$2\"_\"\$3\"\t\"\$1\"\t\"\$2\"\t\"\$3\"\t\"\$4\"\t\"\$5}' | sort > ${VCF2_info}" >> ${script}
echo "join -1 1 -2 1 ${VCF1_info} ${VCF2_info} > ${VCFcompare}_SNPs_inCommon_${chromo}" >> ${script}
SNPs_out=${VCFcompare}_problematicSNPs_${chromo}
echo "cat ${VCFcompare}_SNPs_inCommon_${chromo} | awk '{a=\$2\"\t\"\$3\"\t\"\$4\"\t\"\$5\"\t\"\$6}{b=\$7\"\t\"\$8\"\t\"\$9\"\t\"\$10\"\t\"\$11}a!=b' > ${SNPs_out}" >> ${script}
chmod 711 ${script}
qsub -l h_vmem=3G -o ${script}.o -e ${script}.e ${script}
