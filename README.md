# braker2_singularity
Singularity container for running [BRAKER2](https://github.com/Gaius-Augustus/BRAKER), a container contains all the dependencies needed by BRAKER.

## Installation

Copy this repository
```
git clone https://github.com/SouthernCD/braker2_singularity.git
```

Get license file (named `gm_key_64.gz`) for GeneMark(GeneMark-ES/ET/EP ver 4.69_lic) from [here](http://topaz.gatech.edu/GeneMark/license_download.cgi), and save this file in `braker2_singularity`.

Go to the directory and build container
```
cd braker2_singularity
sudo singularity build braker2.sif braker2.def
```

## Usage

```
singularity run -e braker2.sif --genome input/genome.fa --bam input/RNAseq.bam --softmasking --cores 20
```

For detail see https://github.com/Gaius-Augustus/BRAKER