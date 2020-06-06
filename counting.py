from csv import writer
from csv import reader
import pandas as pd
import argparse

def checklen(input_file, output_file, column):
   ''' How long is the provenance text? '''
   with open(input_file, mode='r') as infile:
       with open(output_file, mode='w') as outfile:
         reader = csv.reader(infile)
         writer = csv.writer(outfile)
         row1 = next(reader)
         pos = row1.index(column)
         writer.writerow(row1 + ["text length"])
         for row in reader:
             writer.writerow(row + [len(row[pos])])

# Method which counts occurrence of specified term within a string (careful when whitespace matters)
# Returns empty sting in case term is 0 times in string
def countAndReturnChar(row, term):
    if row.count(term) > 0:
        return row.count(term)
    else:
        return ''

# Special case of counting occurance, as an opening bracket always needs a closing bracket, too
def countAndReturnBrackets(row):
    term = '['
    if row.count(term) > 0 and row.count(term) == row.count(']'):
        return row.count(term)
        # In case of no closing bracket, ignore opening bracket
    elif row.count(term) > 1:
        return row.count(term) - 1
    else:
        return ''

def countAndReturnWordCount(row):
    # Remove any special characters and digits, lastly calculate minus one, because empty entry is "nan"
    return len(row.lower().replace("0123456789!@#$%^&*()[]{};:,./<>?\|`~-=_+", "").split()) - 1

def main():
    parser = argparse.ArgumentParser('check length of provenance texts')
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    parser.add_argument('column')
    args = parser.parse_args()

    # Additional columns
    questionMarks = []
    brackets = []
    commata = []
    numberOfTo = []
    wordCount = []
    length = []
    df = pd.read_csv(args.input_file)
    provenanceCol = df[args.column]
    for entry in provenanceCol:
        questionMarks.append(countAndReturnChar(str(entry), '?'))
        brackets.append(countAndReturnBrackets(str(entry)))
        commata.append(countAndReturnChar(str(entry), ','))
        numberOfTo.append(countAndReturnChar(str(entry), ' to '))
        wordCount.append(countAndReturnWordCount(str(entry)))
        length.append(len(str(entry)))
    df = df.assign(**{'length': length,'word count': wordCount,'# questionMarks' : questionMarks, '# Brackets' : brackets, '# of commata' : commata, '# of to' : numberOfTo})
    df.to_csv(args.output_file, sep=',')

if __name__ == '__main__':
            main()
