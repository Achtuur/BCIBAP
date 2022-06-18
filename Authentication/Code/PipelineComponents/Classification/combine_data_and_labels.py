import numpy as np
from random import randint

def combine_data_and_labels(data_intervals: list, labels: list):
    if len(data_intervals) != len(labels):
        raise ValueError('Amount of labels does not match amount of data intervals')
    
    return list(zip(data_intervals, labels))

if __name__ == '__main__':
    data = [i for i in range(10)]
    labels = [randint(0,1) for i in range(10)]
    test = combine_data_and_labels(data, labels)
    print(test)