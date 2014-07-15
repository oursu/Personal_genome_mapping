from optparse import OptionParser
import os
import math
from time import gmtime, strftime
import gzip,sys
'''
Merge imputed with phased file. For phased SNPs, do not include the imputation.
'''

def main():
    parser=OptionParser()
    parser.add_option('--imputed',dest='imputed')
    parser.add_option('--phased',dest='phased')
    parser.add_option('--out',dest='outname')
    opts,args=parser.parse_args()

    out=open(opts.outname,'w')

    phased_snps=set()
    if os.path.isfile(opts.phased):
        phased=open(opts.phased)
        for line in iter(phased):
            out.write(line)
            items=line.strip().split('\t')
            snp=items[2]
            phased_snps.add(snp)

    if os.path.isfile(opts.imputed):
        imputed=open(opts.imputed)
        for line in iter(imputed):
            items=line.strip().split('\t')
            snp=items[2]
            if snp in phased_snps:
                continue
            out.write(line)

    out.close()
        
main()
