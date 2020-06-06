# GLAMhack2020
Provenance Text Analysis Project Launched June 5 at GLAMhack2020
https://make.opendata.ch/wiki/event:2020-06

The description of the challenge can be found here: https://hack.glam.opendata.ch/project/7

## Goals
The goal is to automatically analyze, classify, detect patterns in provenance texts that are given in a csv file and rank the results. For detection, quantification and characterization, we tested for red flags that are stated in separate csv sheets. The ranking is supposed to help turn up a deliberately concealed history of looting, forced sale, theft or forgery.

The code is supposed to be abstract enough to be used in other contexts as well. There are currently two approaches to analyze the data that can be combined easily. One focuses on simple counting of red flags. The other one is parsing dates and names to give insight on involved persons and time frames. 

## Ressources
- Dataset with 70,000 art provenance texts for analysis
- Dataset with 1000 Red Flag names
- 10 key words or phrases
Sample files are added in the repository. The original files can be found here: https://www.openartdata.org/2020/06/art-provenance-dataset-text-analysis.html

## How to use
Requirements: Install packages via `pip install -r requirements.txt` and load language model with `python -m spacy download en_core_web_sm`.

The scripts expect a csv dataset with provenance texts as input and a filename for the output file. You can further adjust arguments like the name of the column to check or the path to the red flag files.

We added sample files for testing purposes that can be called with the --sample flag.

## Languages
Python 3

## Contributors

:unlock: :art: :computer:
