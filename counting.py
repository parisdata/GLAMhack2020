from csv import writer
from csv import reader
import pandas as pd
import argparse

# Method which counts occurrence of specified term within a string (careful when whitespace matters)
# Returns empty sting in case term is 0 times in string
def countAndReturnChar(row, term):
    if row.count(term) > 0:
        return row.count(term)
    else:
        return 0

# Special case of counting occurance, as an opening bracket always needs a closing bracket, too
def countAndReturnBrackets(row):
    term = '['
    if row.count(term) > 0 and row.count(term) == row.count(']'):
        return row.count(term)
        # In case of no closing bracket, ignore opening bracket
    elif row.count(term) > 1:
        return row.count(term) - 1
    else:
        return 0

# Counting red flags
def countRedFlags(row, words):
    amount = 0
    for word in words:
        amount = amount + countAndReturnChar(row, word)
    return amount

# creating red flag dict
def createRedFlagDict(rff):
    rfdict = {}
    for index, row in rff.iterrows():
        if row["type of flag"] in rfdict:
            rfdict[row["type of flag"]].append(row["word"])
        else:
            rfdict[row["type of flag"]] = [row["word"]]
    return rfdict

def countAndReturnWordCount(row):
    # Remove any special characters and digits, lastly calculate minus one, because empty entry is "nan"
    return len(row.lower().replace("0123456789!@#$%^&*()[]{};:,./<>?\|`~-=_+", "").split()) - 1

def main():
    parser = argparse.ArgumentParser('check length of provenance texts')
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    parser.add_argument('column')
    parser.add_argument('red_flag_phrase_file')
    parser.add_argument('red_flag_name_file')
    args = parser.parse_args()

    # Preparation
    resultDict = {'length': [], 'wordCount': [], '# of commata': [], '# of to': [], '# red flags total': [], '# red flag names': []}
    df = pd.read_csv(args.input_file)
    rfpf = pd.read_csv(args.red_flag_phrase_file)
    rfnf = pd.read_csv(args.red_flag_name_file)
    rfdict = createRedFlagDict(rfpf)
    nameCol = rfnf["Last Name"]
    provenanceCol = df[args.column]

    # Counting
    for entry in provenanceCol:
        resultDict['length'].append(len(str(entry)))
        resultDict['wordCount'].append(countAndReturnWordCount(str(entry)))
        resultDict['# of commata'].append(countAndReturnChar(str(entry), ','))
        resultDict['# of to'].append(countAndReturnChar(str(entry), ' to '))
        total = 0
        for key, val in rfdict.items():
            amount = countRedFlags(str(entry), val)
            total = total + amount
            if key in resultDict:
                resultDict[key].append(amount)
            else:
                resultDict[key] = [amount]
        names = countRedFlags(str(entry), nameCol)
        total = total + names
        resultDict['# red flag names'].append(names)
        resultDict['# red flags total'].append(total)

    # result csv
    df = df.assign(**resultDict)
    df.to_csv(args.output_file, sep=',')

if __name__ == '__main__':
            main()
