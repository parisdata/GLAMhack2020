#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Julia Beck <j.beck@ub.uni-frankfurt.de>
# 2020

import argparse
import csv

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

def main():
    parser = argparse.ArgumentParser('check length of provenance texts')
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    parser.add_argument('column')
    args = parser.parse_args()
    checklen(input_file=args.input_file, output_file=args.output_file, column=args.column)

if __name__ == '__main__':
            main()
