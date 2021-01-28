# SRA2Virus
This project is going to fish the picornavirus genome sequence from the public SRA database.
Dependence:
1. fastq-dump
2. BBtools (BBduk,BBmap)
3. megahit
4. Blast+
5. diamond

Flow：
sra file -> fastq-dump -> BBduk -> BBmap -> sam file
                 |                             |
                 -> megahit -> diamond         | 
                       |          |            |
                       -> blastn ----------------> results
Usage:
sra2picor.py -s SRRXXXXXXXX SRRXXXXXXXXX ...
-s: sra files with space
