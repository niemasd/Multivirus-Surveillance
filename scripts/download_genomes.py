#! /usr/bin/env python3
'''
Download a collection of NCBI accession numbers as a FASTA
'''

# imports
from Bio import Entrez
from gzip import open as gopen
from pathlib import Path
import argparse

# run script
if __name__ == '__main__':
    # parse user args
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('accession', type=str, nargs='+', help="NCBI Accession Number")
    parser.add_argument('-e', '--email', required=True, type=str, help="Email Address (for Entrez queries)")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output FASTA")
    args = parser.parse_args()
    if args.output != 'stdout':
        args.output = Path(args.output)
        if args.output.exists():
            raise ValueError(f"Output exists: {args.output}")

    # downoad sequences and write to file
    Entrez.email = args.email
    seqs = Entrez.efetch(db='nucleotide', rettype='fasta', id=','.join(s.strip() for s in args.accession)).read()
    if args.output == 'stdout':
        from sys import stdout as out_f
    elif args.output.suffix.lower() == '.gz':
        out_f = gopen(args.output, mode='wt')
    else:
        out_f = open(args.output, mode='wt')
    out_f.write(seqs)
    out_f.close()
