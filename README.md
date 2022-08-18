# braker2_singularity
Singularity container for running [BRAKER2](https://github.com/Gaius-Augustus/BRAKER), a container contains all the dependencies needed by BRAKER.

## Installation

Copy this repository
```
git clone https://github.com/SouthernCD/braker2_singularity.git
```

Go to the directory and download the dependencies
```
cd braker2_singularity
wget https://github.com/Gaius-Augustus/Augustus/releases/download/v3.4.0/augustus-3.4.0.tar.gz
wget https://github.com/bbuchfink/diamond/releases/download/v2.0.15/diamond-linux64.tar.gz
wget https://github.com/gatech-genemark/ProtHint/releases/download/v2.6.0/ProtHint-2.6.0.tar.gz
zcat gm_key_64.gz > ~/.gm_key
```

Build singularity
```
singularity build braker2.sif braker2.def
```

## Usage

```
singularity run --writable-tmpfs braker2.sif braker.pl --genome input/genome.fa --bam input/RNAseq.bam --softmasking --cores 20
```

For detail see https://github.com/Gaius-Augustus/BRAKER