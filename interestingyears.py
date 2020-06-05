import pandas as pd
import csv
import spacy
import dateparser

nlp = spacy.load('en_core_web_sm')

df = pd.read_csv('works.csv', nrows=1000)
df.dropna(inplace=True)
df = df.sample(n=100)

with open('interestingyears.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['url', 'interesting', 'years', 'persons', 'organizations'])
    for _, row in df.iterrows():
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
        # no flags raised yet ...
        interesting = False
        for year in years:
            if year in range(1933, 1946):
                # Nazi period mentioned
                interesting = True
                pass
        if years:
            if min(years) > 1945:
                # first occurance after the war
                interesting = True
            if max(years) < 1930:
                # acquired too early
                interesting = False
            years = [str(year) for year in years]
        csvwriter.writerow([row['url'], str(interesting), ', '.join(years), ', '.join(persons), ', '.join(organizations)])
