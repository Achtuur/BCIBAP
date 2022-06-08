from pathlib import Path
import os
import csv

def csv_to_labels(path_describtion, path_labels):
    description_files = list(path_describtion.iterdir())
    for file in description_files:
        print(file)
        with open(file, newline = '') as f:
            reader = csv.reader(f)
            reader = list(reader)
            reader = reader[::2]
            labels = []
            for segment in reader:
                labels.append(segment[1])
        file = (os.path.basename(file))
        with open(f'{path_labels}\{file}.txt', 'w') as f:
            f.write(str(labels))
                
            



if __name__ == '__main__':
    path_description = Path('.\Pseudowords\\results')
    path_labels = Path('.\Pseudowords\\labels')
    csv_to_labels(path_description, path_labels)