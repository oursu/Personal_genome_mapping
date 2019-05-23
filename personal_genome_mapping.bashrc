#python276=/home/oursu/devtools/Python-2.7.6/python
use .python-2.6.6
python276=/broad/software/free/Linux/redhat_6_x86_64/pkgs/python_2.6.6/bin/python
CODEDIR=/ahg/regevdata/projects/Glioma_scGenetics/tools/mappingDir/Personal_genome_mapping/
use Bowtie
use Tophat
use Samtools
use BWA
#module load bowtie/2.2.1
#module load tophat/2.0.11
#module load samtools/0.1.19
#module load bwa/0.6.1
use Java-1.8
use Picard-Tools
MARKDUPLICATESCMD='java -Xmx2G -jar MarkDuplicates.jar'
