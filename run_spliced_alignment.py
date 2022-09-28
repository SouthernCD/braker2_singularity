#!/usr/bin/env python

import os
import uuid
import sys
from toolbiox.lib.common.os import mkdir, cmd_run, rmdir, multiprocess_running
from toolbiox.lib.common.fileIO import tsv_file_dict_parse
from toolbiox.lib.common.genome.seq_base import read_fasta


def spaln_job(nuc_seq, prot_seq, min_exon_score, tmp_dir, long_gene, long_protein):

    spaln_path = os.path.join(SPALN_DIR, 'spaln')
    spaln_boundary_scorer_path = os.path.join(
        SPALN_DIR, 'spaln_boundary_scorer')
    blosum62_csv_path = os.path.join(SPALN_DIR, 'blosum62.csv')
    spaln_table_path = os.path.join(SPALN_DIR, 'spaln_table')
    os.environ['ALN_TAB'] = spaln_table_path

    if len(nuc_seq.seq) > long_gene or len(prot_seq.seq) > long_protein:
        mode = "-Q7"
    else:
        mode = "-Q3"

    uid = uuid.uuid1().hex
    nuc_file = os.path.join(tmp_dir, '%s_nuc' % uid)
    prot_file = os.path.join(tmp_dir, '%s_prot' % uid)
    out_file = os.path.join(tmp_dir, '%s_out' % uid)

    with open(nuc_file, 'w') as f:
        f.write(">%s\n%s\n" % (nuc_seq.seqname_short(), nuc_seq.seq))

    with open(prot_file, 'w') as f:
        f.write(">%s\n%s\n" % (prot_seq.seqname_short(), prot_seq.seq))

    alignmentLength = len(nuc_seq.seq) * 2

    try:
        spaln_cmd_string = "%s %s -LS -pw -S1 -O1 -l %d %s %s 2> /dev/null | %s -o %s -w 10 -s %s -e %d" % (
            spaln_path, mode, alignmentLength, nuc_file, prot_file, spaln_boundary_scorer_path, out_file, blosum62_csv_path, min_exon_score)
        cmd_run(spaln_cmd_string, cwd=tmp_dir, silence=True)

        with open(out_file, 'r') as f:
            out_string = f.read()
    except:
        out_string = "error"

    try:
        rmdir(nuc_file)
        rmdir(prot_file)
        rmdir(out_file)
    except:
        pass

    return out_string

BIN_DIR = os.path.dirname(os.path.abspath(__file__))
SPALN_DIR = BIN_DIR + "/../dependencies/"

nuc_file = sys.argv[1]
prot_file = sys.argv[2]
list_file = sys.argv[3]
cores = int(sys.argv[4])
min_exon_score = int(sys.argv[5])

long_gene = 30000
long_protein = 15000

# bin = $RealBin

prot = read_fasta(prot_file)[0]
nuc = read_fasta(nuc_file)[0]
pair_list = tsv_file_dict_parse(list_file, fieldnames=['q', 's'])
pair_list = [(pair_list[i]['q'], pair_list[i]['s']) for i in pair_list]

work_dir = os.path.abspath(os.getcwd())
spaln_dir = work_dir + "/spaln"
mkdir(spaln_dir)

args_list = []
for n, p in pair_list:
    nuc[n], prot[p]
    args_list.append((nuc[n], prot[p], min_exon_score, spaln_dir, long_gene, long_protein))

mlt_out = multiprocess_running(spaln_job, args_list, cores, silence=False)

out_file_regions = os.path.join(work_dir, "spaln.regions.gff")

with open(out_file_regions, 'w') as f:

    for m in mlt_out:
        output_string = mlt_out[m]['output']
        f.write(output_string)

spaln_out = os.path.join(work_dir, "spaln.gff")
cmd_run("%s/gff_from_region_to_contig.pl --in_gff %s --seq %s --out_gff %s" % (BIN_DIR, out_file_regions, nuc_file, spaln_out))

rmdir(out_file_regions)
rmdir(spaln_dir)