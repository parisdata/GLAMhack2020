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
            if similarity > 0.85:
                # print (aa, '|', bb, similarity)
                matches.append(bb)
                pass
    return matches

with open('interestingyears.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['url', 'interesting_years', 'years', 'interesting_persons', 'persons', 'interesting_organizations', 'organizations'])
    for _, row in works_df.iterrows():
        p = nlp(str(row['provenance']).replace(';', ' ; '))
        years = []
        persons = []
        organizations = []
        for e in p.ents:
            if e.label_ == 'PERSON':
                persons.append(e.text)
            if e.label_ == 'ORG':
                organizations.append(e.text)
            if e.label_ == 'DATE':
                if date:=dateparser.parse(e.text, languages=['en']):
                    if not years or date.year >= years[-1] and date.year > 1800 and date.year < 2020:
                        years.append(date.year)
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
        # persons
        flagged_persons = find_similar_names(persons, flagged_names)
        flagged_organizations = find_similar_names(organizations, flagged_names)
        csvwriter.writerow([row['url'], str(interesting_year), ', '.join(years), ', '.join(flagged_persons), ', '.join(persons), ', '.join(flagged_organizations), ', '.join(organizations)])
