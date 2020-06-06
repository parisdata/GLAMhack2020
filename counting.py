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
def countRedFlags(row, rfdict):
    amount = 0
    for key in rfdict:
        amount = amount + countAndReturnChar(row, key)
    return amount

def countAndReturnWordCount(row):
    # Remove any special characters and digits, lastly calculate minus one, because empty entry is "nan"
    return len(row.lower().replace("0123456789!@#$%^&*()[]{};:,./<>?\|`~-=_+", "").split()) - 1

def main():
    parser = argparse.ArgumentParser('check length of provenance texts')
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    parser.add_argument('column')
    parser.add_argument('red_flag_file')
    args = parser.parse_args()

    # Additional columns
    questionMarks = []
    brackets = []
    commata = []
    numberOfTo = []
    wordCount = []
    length = []
    redflags = []
    df = pd.read_csv(args.input_file)
    rff = pd.read_csv(args.red_flag_file)
    rfdict = dict(zip(list(rff["word"]),list(rff["type of flag"])))
    provenanceCol = df[args.column]
    for entry in provenanceCol:
        questionMarks.append(countAndReturnChar(str(entry), '?'))
        brackets.append(countAndReturnBrackets(str(entry)))
        commata.append(countAndReturnChar(str(entry), ','))
        numberOfTo.append(countAndReturnChar(str(entry), ' to '))
        wordCount.append(countAndReturnWordCount(str(entry)))
        length.append(len(str(entry)))
        redflags.append(countRedFlags(str(entry),rfdict))
    df = df.assign(**{'length': length,'word count': wordCount,'# red flags' : redflags, '# questionMarks' : questionMarks, '# Brackets' : brackets, '# of commata' : commata, '# of to' : numberOfTo})
    df.to_csv(args.output_file, sep=',')

if __name__ == '__main__':
            main()
