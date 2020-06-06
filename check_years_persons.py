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


year_pattern = re.compile(r'[12][0-9]{3}')
century_pattern = re.compile(r'[12][0-9]th\s+c')
circa_pattern = re.compile(r'c[a]*\.')
dash_pattern = re.compile(r'[-–—]')

def find_similar_names(a:list, b:list) -> list:
    matches = []
    for aa in a:
        for bb in b:
            ratio = fuzz.ratio(aa.lower().replace(' ', ''), bb.lower().replace(' ', ''))
            if ratio > 80 and bb not in matches:
                matches.append(bb)
    return matches

def find_creation_year(date_str:str, nlp) -> int:
    # delete circas
    date_str = circa_pattern.sub('', date_str)
    date_str = dash_pattern.sub(' - ', date_str)
    date = dateparser.parse(date_str, languages=['en'])
    if date and date.year in range(1000, 2030):
        return date.year
    century_match = century_pattern.search(date_str)
    if century_match:
        year = int(century_match.group(0)[:2]) * 100 + 50
        return year
    years = []
    for e in nlp(date_str).ents:
        if e.label_ == 'DATE':
            date = dateparser.parse(e.text, languages=['en'])
            if date:
                years.append(date.year)
    if years:
        return max(years)
    return 0

def find_accession_year(accession_number:str) -> str:
    if not pd.isnull(accession_number):
        accession_match = year_pattern.search(accession_number)
        if accession_match:
            accession_year = accession_match.group(0)
            rests = accession_number.split(accession_year)
            if rests[0] and rests[0][-1:].isnumeric():
                return None
            if rests[1] and rests[1][:1].isnumeric():
                return None
            return accession_year
    return None

def find_provenance_gap(years:list) -> int:
    # Is there a gap for the time from 1933 to 1945 and how big is it?
    if years:
        # make sure there are no years between 1934 and 1944 in the list
        for y in range(1934, 1945):
            if y in years:
                return 0
        # find last year up until 1933
        a_year = 0
        for y in years:
            if y <= 1933:
                a_year = y
        # find first year from 1945
        b_year = 0
        for y in years[::-1]:
            if y >= 1945:
                b_year = y
        if a_year and b_year:
            return b_year - a_year
    return 0

def parse_lines(works_df:pd.DataFrame, flagged_names:list, output:str):
    nlp = spacy.load('en_core_web_sm')
    with open(output, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['url', 'interesting_years', 'provenance_gap', 'years', 'interesting_actors', 'actors'])
        for _, row in tqdm(works_df.iterrows(), total=works_df.shape[0]):
            provenance = str(row['provenance']).replace(';', ' ; ')
            # delete live dates
            provenance = re.sub(r'\([12][0-9]{3}\.*[-–—]\.*[12][0-9]{3}\)', '', provenance)
            p = nlp(provenance)
            years = []
            actors = []
            accession_year = find_accession_year(row['accnum'])
            if 'date' in row:
                creation_year = find_creation_year(row['date'], nlp)
                if creation_year != 0:
                    years.append(creation_year)
            for e in p.ents:
                if e.label_ in ['PERSON', 'ORG']:
                    actors.append(e.text)
                if e.label_ == 'DATE':
                    date = dateparser.parse(e.text, languages=['en'])
                    if date:
                        if (not years or date.year >= years[-1]) and date.year not in years and date.year > 1800 and date.year < 2020 and (not accession_year or date.year < int(accession_year)):
                            years.append(date.year)
            if accession_year:
                years.append(int(accession_year))
            # years
            # no flags raised yet ...
            interesting_year = False
            for year in years:
                if year in range(1933, 1946):
                    # Nazi period mentioned
                    interesting_year = True
                    pass
            if years:
                if min(years) > 1945:
                    # first occurance after the war
                    interesting_year = True
                if max(years) < 1930:
                    # acquired too early
                    interesting_year = False
            provenance_gap = find_provenance_gap(years)
            years = [str(year) for year in years]
            # actors
            flagged_actors = find_similar_names(set(actors), flagged_names)
            csvwriter.writerow([row['url'], str(interesting_year), str(provenance_gap), ', '.join(years), ', '.join(flagged_actors), ', '.join(actors)])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sample', help='process random sample only', type=int, default=0)
    parser.add_argument('-iw', '--inputworks', help='csv with works', type=str, default='works.csv')
    parser.add_argument('-ip', '--inputpersons', help='csv with persons', type=str, default='red-flags-names.csv')
    parser.add_argument('-o', '--output', help='process random sample only', type=str, default='years-persons.csv')
    args = parser.parse_args()
    if args.sample == 0:
        works_df = pd.read_csv(args.inputworks)
    else:
        works_df = pd.read_csv(args.inputworks, nrows=args.sample*4)
    works_df.dropna(inplace=True)
    if args.sample > 0:
        works_df = works_df.sample(n=min(args.sample, works_df.shape[0]))
    works_df.replace(to_replace='\n', value=' ', regex=True, inplace=True)

    names_df = pd.read_csv(args.inputpersons)
    flagged_names = names_df['First Name Last Name'].tolist()
    flagged_names = [name.strip() for name in flagged_names]

    parse_lines(works_df, flagged_names, args.output)

if __name__ == '__main__':
            main()
