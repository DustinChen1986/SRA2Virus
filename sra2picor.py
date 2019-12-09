import os
srafiles = ['SRR4254090', 'SRR4254091', 'SRR4254092']
for sra in srafiles:
    os.system('fastq-dump -O /media/sf_G/picornavirus/ --split-3 /media/sf_G/picornavirus/'+sra+'.sra')
pairend = []
single = []
for root, dirs, files in os.walk("/media/sf_G/picornavirus/"):
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
        os.system('trimmomatic PE -threads 11 -phred33 /media/sf_G/picornavirus/' #trim
        +i+'_1.fastq /media/sf_G/picornavirus/'+i+'_2.fastq /media/sf_G/picornavirus/'
        +i+'_1_p.fastq /media/sf_G/picornavirus/'+i+'_1_u.fastq /media/sf_G/picornavirus/'+i+'_2_p.fastq /media/sf_G/picornavirus/'+i+'_2_u.fastq '
        +'ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36')
        os.system('rm /media/sf_G/picornavirus/'+i+'_1.fastq /media/sf_G/picornavirus/'+i+'_2.fastq /media/sf_G/picornavirus/' #remove fastq
        +i+'_1_u.fastq /media/sf_G/picornavirus/'+i+'_2_u.fastq')
        fastq1 +='/media/sf_G/picornavirus/'+i+'_1_p.fastq,'
        fastq2 +='/media/sf_G/picornavirus/'+i+'_2_p.fastq,'
    os.system('megahit -t 11  -o megahit_out '+fastq1[:-1]+' '+fastq2[:-1])
    os.system('mv megahit_out /media/sf_G/picornavirus/')
    os.system('diamond blastx -p 11 -d /media/sf_G/picornavirus/cds.dmnd -q /media/sf_G/picornavirus/megahit_out/final.contigs.fa --outfmt 6 -o diamond.txt')
    os.system('mv diamond.txt /media/sf_G/picornavirus/megahit_out/')
def single_assemble(single):
    fastq = ''
    for i in single:
        os.system('trimmomatic SE -threads 11 -phred33 /media/sf_G/picornavirus/'+i+'.fastq /media/sf_G/picornavirus/'+i+'_s.fastq '
        + 'ILLUMINACLIP:TruSeq3-SE:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36')
        os.system('rm /media/sf_G/picornavirus/'+i+'.fastq')
        fastq += '/media/sf_G/picornavirus/'+i+'_s.fastq,'
    print(fastq)
    os.system('megahit -t 11 -o megahit_out -r '+fastq[:-1])
    os.system('mv megahit_out /media/sf_G/picornavirus/')
    os.system('diamond blastx -p 11 -d /media/sf_G/picornavirus/cds.dmnd -q /media/sf_G/picornavirus/megahit_out/final.contigs.fa --outfmt 6 -o diamond.txt')
    os.system('mv diamond.txt /media/sf_G/picornavirus/megahit_out/')
if pairend:
    pairend_assemble(pairend)
elif single:
    single_assemble(single)