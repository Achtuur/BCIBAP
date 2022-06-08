from Frequencytagging import tagging
import numpy as np
import csv
import argparse
from datetime import datetime
import os

my_parser = argparse.ArgumentParser(description="Code to frequency tag a password")
my_parser.add_argument('-pw',
                        required=True,
                        metavar='password',
                        type=str,
                        help='The password to tag, add words with spaces in between and within brackets'    
                    )
my_parser.add_argument('-freq',
                        required=False,
                        metavar='-frequency',
                        type=int,
                        help='The frequency of the tagged password'    
                    )
my_parser.add_argument('-time',
                        required=False,
                        metavar='-time',
                        type=int,
                        help='The duration of the tagging',
                        default=15
)
my_parser.add_argument('-R',
                        required=False,
                        metavar='-Response Recognition',
                        type=str,
                        help='something for response recognition, nothing for tagging only',
                        default=False
)
my_parser.add_argument('-name',
                        required=True,
                        metavar='Subject name',
                        type=str,
                        help='Name of the person who is experimented on',
                        default=False
)
my_parser.add_argument('-take',
                        required=True,
                        metavar='Take',
                        type=str,
                        help='The nth time that this subject does the experiment',
                        default=False
)
args = my_parser.parse_args()

#Information for tagging
chosen_words = args.pw
time = args.time
frequency = args.freq
responserecogntion = args.R

if __name__ == '__main__':

    date = str(datetime.now())[0:10]
    filename = f'.\\results\\Step3\\{args.name}_{date}_ft3_take{args.take}'
    if os.path.exists(f'{filename}.csv'):
        print('filename already exists')
        exit()
        
    bitjes, start_time, words = tagging(step = '3', time = 1, chosen_words = args.pw, color = '000')
    print(words)

    
    words.append(start_time)
    bitjes.append(' ')
    all_data = [words, bitjes]
    all_data = np.array(all_data).T.tolist()

    with open(f'{filename}.csv', 'w') as f:
      
    # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerows(all_data)