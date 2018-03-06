#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    target_categiry = sys.argv[2]
    
    print('Handle file: {0}'.format(filename))
    print('Extrack products for category id: {0}'.format(target_categiry))
    
    product_names = []
    
    with open(filename, newline='', encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvreader:
            if row[-2] == target_categiry:
                product_names.append(row[1])
    
    with open('Category_{0}_raw_names.csv'.format(target_categiry),'wt', encoding="utf8") as file:
        for name in product_names:
            file.write("{0},{1}".format(name,target_categiry))
            file.write('\n')
    
    print('Extrackted names: {0}'.format(len(product_names)))