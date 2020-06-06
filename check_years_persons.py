#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Birk Weiberg <birk.weiberg@sapa.swiss>
# 2020

# download model first: python -m spacy download en_core_web_sm

import re
import pandas as pd
import csv
import spacy
import dateparser
import difflib

nlp = spacy.load('en_core_web_sm')

works_df = pd.read_csv('works.csv', nrows=5000)
works_df.dropna(inplace=True)
works_df = works_df.sample(n=1000)

names_df = pd.read_csv('red-flags-names.csv')
flagged_names = names_df['First Name Last Name'].tolist()
flagged_names = [name.strip() for name in flagged_names]

def find_similar_names(a:list, b:list) -> list:
    matches = []
    for aa in a:
        for bb in b:
            similarity = difflib.SequenceMatcher(None, aa.lower().replace(' ', ''), bb.lower().replace(' ', '')).ratio()
            if similarity > 0.7:
                matches.append(f'{bb}|{similarity}')
                pass
    return matches

year_pattern = re.compile(r'[12][0-9]{3}')

def find_accession_year(accession_number:str) -> str:
    if not pd.isnull(accession_number):
        if accession_match:=year_pattern.search(accession_number):
            accession_year = accession_match.group(0)
            rests = accession_number.split(accession_year)
            if rests[0] and rests[0][-1:].isnumeric():
                return None
            if rests[1] and rests[1][:1].isnumeric():
                return None
            return accession_year
    return None

with open('interestingyears.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['url', 'interesting_years', 'years', 'interesting_actors', 'actors'])
    for _, row in works_df.iterrows():
        p = nlp(str(row['provenance']).replace(';', ' ; '))
        years = []
        actors = []
        accession_year = find_accession_year(row['accnum'])
        for e in p.ents:
            if e.label_ in ['PERSON', 'ORG']:
                actors.append(e.text)
            if e.label_ == 'DATE':
                if date:=dateparser.parse(e.text, languages=['en']):
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
            years = [str(year) for year in years]
        # actors
        flagged_actors = find_similar_names(set(actors), flagged_names)
        csvwriter.writerow([row['url'], str(interesting_year), ', '.join(years), ', '.join(flagged_actors), ', '.join(actors)])
