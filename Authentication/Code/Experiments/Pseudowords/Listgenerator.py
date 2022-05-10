import csv
import random
import numpy as np


def listgenerator(length):
    with open('woorden.csv', newline='') as f:
        reader = csv.reader(f)
        echt = list(reader)

    with open('pseudowords.csv', newline='') as f:
        reader = csv.reader(f)
        pseudo = list(reader)
        
    random.shuffle(echt)
    random.shuffle(pseudo)

    numbers = list(range(1,length + 1))
    numbers = np.array(numbers)

    j = 0
    words = [0] * length
    bitjes = [0] * length
    for i in numbers:   
        n = random.randint(1,2)
        if n == 1:
            words[j] = echt[i]
            bitjes[j] = 1
        else:
            words[j] = pseudo[i]
            bitjes[j] = 0
        j = j + 1
    
    return words, bitjes

# words, bitjes = listgenerator(lenght)
# print(words)
# print(bitjes)


# file = open('wordlist.csv', 'w+', newline ='') 
# with file:     
#     write = csv.writer(file) 
#     write.writerows(words) 

    

