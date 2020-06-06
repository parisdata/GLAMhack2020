# GLAMhack2020
Provenance Text Analysis Project Launched June 5 at GLAMhack2020
https://make.opendata.ch/wiki/event:2020-06

The description of the challenge can be found here: https://hack.glam.opendata.ch/project/7

## Goals
The goal is to automatically analyze, classify, detect patterns in provenance texts that are given in a csv file and rank the results. For detection, quantification and characterization, we tested for red flags that are stated in separate csv sheets. The ranking is supposed to help turn up a deliberately concealed history of looting, forced sale, theft or forgery.

The code is supposed to be abstract enough to be used in other contexts as well.

## Ressources
- Dataset with 70,000 art provenance texts for analysis
- Dataset with 1000 Red Flag names
- 10 key words or phrases
Sample files are added in the repository. The original files can be found here: https://www.openartdata.org/2020/06/art-provenance-dataset-text-analysis.html

## Languages
Python 3, install packages via `pip install -r requirements.txt` and load language model with `python -m spacy download en_core_web_sm`.

## Contributors

:unlock: :art: :computer:
