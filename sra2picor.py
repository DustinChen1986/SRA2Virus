import os
import argparse

parser = argparse.ArgumentParser(description='SRA fishing picornavirus')
parser.add_argument('-s', '--sra', type=str, help='SRA file, separate with comma')
parser.add_argument('-f', '--folder', type=str, default='./', help='SRA folder')
parser.add_argument('-t', '--threads', type=int, default=12, help='CPU threads')
args = parser.parse_args()
srafiles = args.sra.split(',')
srafolder = args.folder
threads = args.threads

for sra in srafiles:
    os.system('fastq-dump --split-3 '+srafolder+sra)
pairend = []
single = []
files = os.listdir("./")
for sra in srafiles:
    if sra+'_2.fastq' in files:
        pairend.append(sra)
    else:
        single.append(sra)
pairend=list(set(pairend))
single=list(set(single))
def pairend_assemble(pairend):
    fastq1='-1 '
    fastq2='-2 '
    for i in pairend:
        os.system('trimmomatic PE -threads '+threads+' -phred33 ' #trim
        +i+'_1.fastq '+i+'_2.fastq '
        +i+'_1_p.fastq '+i+'_1_u.fastq '+i+'_2_p.fastq '+i+'_2_u.fastq '
        +'ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36')
        os.system('rm '+i+'_1.fastq '+i+'_2.fastq ' #remove fastq
        +i+'_1_u.fastq '+i+'_2_u.fastq')
        fastq1 += i+'_1_p.fastq,'
        fastq2 += i+'_2_p.fastq,'
    os.system('megahit -t '+threads+' -o megahit_out '+fastq1[:-1]+' '+fastq2[:-1])
    os.system('diamond blastx -p '+threads+' -d cds.dmnd -q ./megahit_out/final.contigs.fa --outfmt 6 -o diamond.txt')
def single_assemble(single):
    fastq = ''
    for i in single:
        os.system('trimmomatic SE -threads '+threads+' -phred33 '+i+'.fastq '+i+'_s.fastq '
        + 'ILLUMINACLIP:TruSeq3-SE:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36')
        os.system('rm '+i+'.fastq')
        fastq += i+'_s.fastq,'
    print(fastq)
    os.system('megahit -t '+threads+' -o megahit_out -r '+fastq[:-1])
    os.system('diamond blastx -p '+threads+' -d cds.dmnd -q ./megahit_out/final.contigs.fa --outfmt 6 -o diamond.txt')
if pairend:
    pairend_assemble(pairend)
elif single:
    single_assemble(single)
