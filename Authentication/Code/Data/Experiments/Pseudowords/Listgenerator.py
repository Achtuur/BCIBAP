import csv
import random
import numpy as np


def listgenerator(length, orderd = True):
    with open('woorden.csv', newline='') as f:
        reader = csv.reader(f)
        echt = list(reader)[:int(length/2)]

    with open('pseudowords.csv', newline='') as f:
        reader = csv.reader(f)
        pseudo = list(reader)[:int(length/2)]
        
    random.shuffle(echt)
    random.shuffle(pseudo)

    numbers = list(range(1,length + 1))
    numbers = np.array(numbers)

    j = 0


    words = echt + pseudo
    bitjes = ([1] * len(echt)) + ([0] * len(pseudo))

    if orderd == False:
        c = list(zip(words, bitjes))

        random.shuffle(c)

        words, bitjes = zip(*c)
    
    return words, bitjes

# words, bitjes = listgenerator(lenght)
# print(words)
# print(bitjes)


# file = open('wordlist.csv', 'w+', newline ='') 
# with file:     
#     write = csv.writer(file) 
#     write.writerows(words) 

    

