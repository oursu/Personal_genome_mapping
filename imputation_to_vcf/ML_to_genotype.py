from optparse import OptionParser
import os
import math
from time import gmtime, strftime
import gzip,sys
'''
Make vcf for imputed individuals.
'''

def main():
    parser=OptionParser()
    parser.add_option('--info_threshold',dest='info_t',default='0.8')
    parser.add_option('--impute2_almostVCF',dest='impute2_almostVcf')
    parser.add_option('--out',dest='outname')
    opts,args=parser.parse_args()

    in_file=open(opts.impute2_almostVcf)
    out=open(opts.outname,'w')
    info_t=float(opts.info_t)
    first=True

    for line in iter(in_file):
        if first:
            out.write(line)
            first=False
            continue
        items=line.strip().split()
        info_score=items[5]
        if float(info_score)<info_t:
            continue
        ll=items[9]
        out.write('\t'.join(items[0:9])+'\t'+get_genotype_from_ll(ll)+'\n')

def get_genotype_from_ll(three_values):
    vals=three_values.split(',')
    val_ref=float(vals[0])
    val_het=float(vals[1])
    val_alt=float(vals[2])
    if val_ref>=val_het and val_ref>=val_alt:
        return '0/0'
    if val_het>=val_ref and val_het>=val_alt:
        return '1/0'
    if val_alt>=val_ref and val_alt>=val_het:
        return '1/1'
    return './.'

                


main()
