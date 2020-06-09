#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Birk Weiberg <birk.weiberg@sapa.swiss>
# 2020

# download model first: python -m spacy download en_core_web_sm

import re
import argparse
import pandas as pd
import csv
from tqdm import tqdm
import spacy
import dateparser
from fuzzywuzzy import fuzz


def parse_lines(works_df:pd.DataFrame, output:str):
    names = []
    nlp = spacy.load('en_core_web_sm')
    for _, row in tqdm(works_df.iterrows(), total=works_df.shape[0]):
        provenance = str(row['provenance']).replace(';', ' ; ')
        # delete live dates
        provenance = re.sub(r'\([12][0-9]{3}\.*[-–—]\.*[12][0-9]{3}\)', '', provenance)
        p = nlp(provenance)
        for e in p.ents:
            if e.label_ in ['PERSON', 'ORG'] and e.text not in names:
                names.append(e.text)
    with open(output, 'w') as f:
        for n in sorted(names):
            f.write(f'{n}\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sample', help='process random sample only', type=int, default=0)
    parser.add_argument('-i', '--input', help='csv with works', type=str, default='works.csv')
    parser.add_argument('-o', '--output', help='process random sample only', type=str, default='years-persons.csv')
    args = parser.parse_args()
    if args.sample == 0:
        works_df = pd.read_csv(args.input)
    else:
        works_df = pd.read_csv(args.input, nrows=args.sample*4)
    works_df.dropna(inplace=True)
    if args.sample > 0:
        works_df = works_df.sample(n=min(args.sample, works_df.shape[0]))
    works_df.replace(to_replace='\n', value=' ', regex=True, inplace=True)

    parse_lines(works_df, args.output)

if __name__ == '__main__':
            main()
