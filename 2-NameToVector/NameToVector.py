# -*- encoding: utf-8 -*-
import sys
import csv
from sklearn.feature_extraction.text import TfidfVectorizer

def read_dataset(filename):
    names = []
    labels = []
    
    with open(filename, newline='', encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvreader:
            #print('Name is {0}'.format(row[0]))
            names.append(row[0])
            labels.append(row[1])
    
    return names, labels
    
def build_vectorizator(names):
    #create the transform
    vectorizer = TfidfVectorizer(stop_words='english')
    # tokenize and build vocab
    vectorizer.fit(names)
    
    # summarize
    print('vocabulary is \n')
    print(vectorizer.vocabulary_)
    print('-----\n')
    
    print('Some param\n')
    print(vectorizer.idf_)
    print('-----\n')
    
    # encode document
    #vector = vectorizer.transform([names[0]])
    
    # summarize encoded vector
    #print('vector shape\n')
    #print(vector.shape)
    #print('-----\n')
    
    #print('vector val\n')
    #print(vector.toarray())
    #print('-----\n')
    
    return vectorizer
    
def transform_names(vectorizer, names):
    vectors = []
    
    for name in names:
        vector = vectorizer.transform([name])
        vectors.append(vector)
    return vectors
    
def get_dataset_length(vectors, labels):
    if len(vectors) != len(labels):
        print('Error: Vectors and labels must be equals by length')
        sys.exit()
    else:
        return len(vectors)
    
def vec_to_string(vector):
    vec_arr = vector.toarray()
    result_str = ''
    
    for i in range(0, vector.shape[1]):
        result_str += '{0},'.format(vec_arr[0,i])
    return result_str
    
if __name__ == "__main__":
    filename = sys.argv[1]
    
    names, labels = read_dataset(filename)
    
    vectorizer = build_vectorizator(names)
    vectors = transform_names(vectorizer, names)
    
    vector_len = vectors[0].shape[1]
    print('Vector length = {0}'.format(vector_len))
    
    n = get_dataset_length(vectors,labels)
    print('Dataset length = {0}'.format(n))
    
    output_strings = []
    
    for i in range(0,n):
        features = vec_to_string(vectors[i])
        output_strings.append('{0}{1}'.format(features, labels[i]))
    
    with open('Transformed_dataset.csv','wt', encoding="utf8") as file:
        for str in output_strings:
            file.write(str)
            file.write('\n')
    