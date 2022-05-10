import csv
import random
import numpy as np

with open('woorden.csv', newline='') as f:
    reader = csv.reader(f)
    echt = list(reader)

with open('pseudowords.csv', newline='') as f:
    reader = csv.reader(f)
    pseudo = list(reader)

numbers = list(range(1,51))
random.shuffle(numbers)
numbers = np.array(numbers)

j = 0
words = [0] * 50
for i in numbers:   
    n = random.randint(1,2)
    print(n)
    if n == 1:
        words[j] = echt[i]
    else:
        words[j] = pseudo[i]
    j = j + 1

print(words)


file = open('wordlist.csv', 'w+', newline ='') 
with file:     
    write = csv.writer(file) 
    write.writerows(words) 

    

