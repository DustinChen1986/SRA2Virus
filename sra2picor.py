#!/usr/bin/env python
import os
from Bio import SeqIO
import argparse
parser = argparse.ArgumentParser(description='SRA to piconavirus')
parser.add_argument('-s', '--sra', nargs='+', type=str, help='sra file')
args = parser.parse_args()
sras = args.sra

def pairend_assemble(pairend):
    trim = pairend.join(['bbduk.sh in=','_1.fastq in2=','_2.fastq out=','_1_trim.fastq out2=','_2_trim.fastq ref=adapters.fa ktrim=r k=23 mink=11 hdist=1 tpe tbo qtrim=r trimq=10 maq=10 minlen=30 maxns=3 trimpolya=3 threads=12'])
    print(trim)
    os.system(trim)
    print('rm '+pairend+'_1.fastq '+pairend+'_2.fastq')
    os.system('rm '+pairend+'_1.fastq '+pairend+'_2.fastq') #remove fastq
    fastq1 = pairend+'_1_trim.fastq'
    fastq2 = pairend+'_2_trim.fastq'
#    bowtie2 = 'bowtie2 -p 11 --no-unal -x picornavirus -1 '+fastq1+' -2 '+fastq2+' -S '+sra+'.sam'
#    print(bowtie2)
    bbmap = 'bbmap.sh noheader=T in='+fastq1+' in2='+fastq2+' outm='+sra+'.sam'
    print(bbmap)
    os.system(bbmap)
    megahit = 'megahit -t 12  -o ./'+pairend+'_megahit --out-prefix '+pairend+' -1 ' +fastq1+' -2 '+fastq2
    print(megahit)
    os.system(megahit)
    print('rm '+pairend+'_1_trim.fastq '+pairend+'_2_trim.fastq')
    os.system('rm '+pairend+'_1_trim.fastq '+pairend+'_2_trim.fastq') #remove trimed fastq
    diamond = pairend.join(['diamond blastx -p 12 -d picornavirus.dmnd -q ./','_megahit/','.contigs.fa --outfmt 6 -o ','_diamond.txt'])
    print(diamond)
    os.system(diamond)
    blastn = pairend.join(['blastn -db picornavirus_nucl_genome -outfmt 6 -out ','_blastn.txt -num_threads 12 -query ./','_megahit/','.contigs.fa '])
    print(blastn)
    os.system(blastn)
def single_assemble(single):
    trim = single.join(['bbduk.sh in=','.fastq out=','_trim.fastq ref=adapters.fa ktrim=r k=23 mink=11 hdist=1 tpe tbo qtrim=r trimq=10 maq=10 minlen=30 maxns=3 trimpolya=3 threads=12'])
    print(trim)
    os.system(trim)
    print('rm '+single+'.fastq')
    os.system('rm '+single+'.fastq')
    fastq = single+'_trim.fastq'
#    bowtie2 = 'bowtie2 -p 11 --no-unal -x picornavirus -U '+fastq+' -S '+single+'.sam'
    bbmap = 'bbmap.sh noheader=T in='+fastq+' outm='+sra+'.sam'
    print(bbmap)
    os.system(bbmap)
    megahit = 'megahit -t 12 -o ./'+single+'_megahit --out-prefix '+single+' ' + '-r '+fastq
    print(megahit)
    os.system(megahit)
    print('rm '+single+'_trim.fastq')
    os.system('rm '+single+'_trim.fastq')
    diamond = single.join(['diamond blastx -p 12 -d picornavirus.dmnd -q ./','_megahit/','.contigs.fa --outfmt 6 -o ','_diamond.txt'])
    print(diamond)
    os.system(diamond)
    blastn = single.join(['blastn -db picornavirus_nucl_genome -outfmt 6 -out ','_blastn.txt -num_threads 12 -query ./','_megahit/','.contigs.fa'])
    print(blastn)
    os.system(blastn)

for sra in sras:
    try:
        os.system('fastq-dump --split-e '+sra)
        if sra+'_2.fastq' in os.listdir("./"):
            pairend_assemble(sra)
        else:
            single_assemble(sra)
        seqlist = list(set([line.split('\t')[0] for line in open(sra+'_blastn.txt')] + [line.split('\t')[0] for line in open(sra+'_diamond.txt')]))
        print(seqlist)
        with open(sra+'_virus.fas', 'w') as res:
            for seq in SeqIO.parse(sra.join(['./','_megahit/','.contigs.fa']), 'fasta'):
                if seq.id in seqlist:
                    SeqIO.write(seq, res, 'fasta')
        with open(sra+'_sam.txt', 'w') as sam:
            samlist = list(set([line.split('\t')[2] for line in open(sra+'.sam') if line.split('\t')[9].count('A')/len(line.split('\t')[9]) <= 0.8]))
            for seq in SeqIO.parse('genome_base.fas', 'fasta'):
                if seq.id in samlist:
                    print(seq.description, file = sam)
    except:
        pass
