# -*- encoding: utf-8 -*-
import sys
import csv
import numpy as np

if __name__ == "__main__":
    filename = sys.argv[1]
    
    dataset = []
    
    #with open(filename, newline='', encoding="utf8") as csvfile:
    #    for line in csvfile:
    #        dataset.append(line)
            
    with open(filename, newline='', encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvreader:
            dataset.append(row)
    
    np.random.shuffle(dataset)
    
    with open('Shuffled_dataset.csv','wt', encoding="utf8") as file:
        for row in dataset:
            file.write(','.join(row))
            file.write('\n')