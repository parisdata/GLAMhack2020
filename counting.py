from csv import writer
from csv import reader
import pandas as pd 

# Todo: make dynamic
filename = "testingCounts.csv"
column = "provenance"

# Additional columns
questionMarks = []
brackets = []
commata = []
numberOfTo = []
wordCount = []
 
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

file = r'testingCounts.csv'
df = pd.read_csv(file)
provenanceCol = df[column]
for entry in provenanceCol:
    questionMarks.append(countAndReturnChar(str(entry), '?'))
    brackets.append(countAndReturnBrackets(str(entry)))
    commata.append(countAndReturnChar(str(entry), ','))
    numberOfTo.append(countAndReturnChar(str(entry), ' to '))
    wordCount.append(countAndReturnWordCount(str(entry)))

df = df.assign(**{'word count': wordCount,'# questionMarks' : questionMarks, '# Brackets' : brackets, '# of commata' : commata, '# of to' : numberOfTo})
df.to_csv('output_test.csv', sep=',')