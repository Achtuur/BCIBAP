import sys
import platform
import numpy as np
import csv
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.preprocessing import normalize
import random


if platform.system() == "Windows":
    sys.path.append(str(Path('PipelineComponents/Preprocessing').resolve()))
    sys.path.append(str(Path('PipelineComponents/FeatureExtraction').resolve()))
    sys.path.append(str(Path('Data/ExperimentResults').resolve()))
    sys.path.append(str(Path('Data').resolve()))
    sys.path.append(str(Path('PipelineComponents/Classification').resolve()))
else:
    sys.path.append(str(Path('../../PipelineComponents/Preprocessing').resolve()))
    sys.path.append(str(Path('../../PipelineComponents/FeatureExtraction').resolve()))
    sys.path.append(str(Path('../../PipelineComponents/Classification').resolve()))
    sys.path.append(str(Path('../../Data/ExperimentResults').resolve()))
    sys.path.append(str(Path('../../Data').resolve()))

from PreprocessingPipeline import PreprocessingPipeline
from Visualize import DataPlot 
from Filters import Filter
from crop import crop
from FeaturesLos import right_hemisphere_difference_ratio

if __name__ == '__main__':

    # Initialise exp 1
    data = np.load(Path('../../Data/ExperimentResults/recorded_data/recordings_numpy/Joos/OpenBCISession_Joos_exp_pseudo2_1s_take1.npy'))
    data_filtered = PreprocessingPipeline(data).start()
    data_cropped = crop(data_filtered, 2, 250)
    data_cropped = list(map(lambda x: Filter.remove_bad_channels(x), data_cropped))
    data_cropped = [x for x in data_cropped if x is not None]
    data_to_analyse = np.concatenate(data_cropped)

    data_pw_words = data_to_analyse[:20*250,:]
    data_words = data_to_analyse[20*250:,:]
    
    # Initialise exp 2
    data = np.load(Path('../../Data/ExperimentResults/recorded_data/recordings_numpy/Joos/OpenBCISession_Joos_exp_pseudo2_1s_take2.npy'))
    data_filtered = PreprocessingPipeline(data).start()
    data_cropped = crop(data_filtered, 2, 250)
    data_cropped = list(map(lambda x: Filter.remove_bad_channels(x), data_cropped))
    data_cropped = [x for x in data_cropped if x is not None]
    data_to_analyse = np.concatenate(data_cropped)

    data_pw_words = np.append(data_pw_words, data_to_analyse[:20*250,:], axis=0)
    data_words = np.append(data_words, data_to_analyse[20*250:,:], axis=0)

    # Initialise exp 3 
    data = np.load(Path('../../Data/ExperimentResults/recorded_data/recordings_numpy/Joos/OpenBCISession_Joos_exp_pseudo2_1s_take3.npy'))
    data_filtered = PreprocessingPipeline(data).start()
    data_cropped = crop(data_filtered, 2, 250)
    data_cropped = list(map(lambda x: Filter.remove_bad_channels(x), data_cropped))
    data_cropped = [x for x in data_cropped if x is not None]
    data_to_analyse = np.concatenate(data_cropped)


    data_pw_words = np.append(data_pw_words, data_to_analyse[:20*250,:], axis=0)
    data_words = np.append(data_words, data_to_analyse[20*250:,:], axis=0)

    # These intervals can be devided by 60
    intervals = [x for x in range(1,61) if 60 % x == 0]

    results = {
        '1' : 0,
        '2' : 0,
        '3' : 0,
        '4' : 0,
        '5' : 0,
        '6' : 0,
        '10' : 0,
        '12' : 0,
        '15' : 0,
        '20' : 0,
        '30' : 0,
        '60' : 0
    }
    for interval in intervals:
        ratios = []
        data_words_list = crop(data_words, interval, 250)
        data_pw_list = crop(data_pw_words, interval, 250)
        random.shuffle(data_pw_list) 

        for pw_data_point in data_pw_list:
            ratios.append(right_hemisphere_difference_ratio(pw_data_point, data_words_list, (25,35)))

        total = len(ratios)
        score = 0
        for ratio in ratios:
            if ratio >= 1:
                score += 1
        results[str(interval)] = score/total

    values = [100*x for x in results.values()] 
    X = [x for x in range(0, 12)]
    p = np.polyfit(X, values, 2)


    plt.bar(results.keys() ,[100*x for x in results.values()], label="Feature prediction score")
    plt.title('Prediction score for different measurement intervals', fontsize=16)
    plt.xlabel('Measurement Interval [s]', fontsize=16)
    plt.ylabel('Score [%]', fontsize=16)
    plt.plot(X, np.multiply(p[0], np.power(X, 2)) + np.multiply(p[1], X) + p[2], color="orange", label="Fit  of the score values")
    plt.legend(fontsize=16)
    # plt.show(block=True)
    plt.savefig('right_hemisphere_difference.jpg', dpi=200)


# data_words = data_to_analyse[:20*250,:]
    # data_pw_words = data_to_analyse[20*250:,:]
    # data_words_list = crop(data_words, 4, 250)
    # data_pw_list = crop(data_pw_words, 4, 250)

    # ratios1 = []

    # for pw_data_point in data_pw_list:
    #     ratios1.append(left_hemisphere_difference_ratio(pw_data_point, data_words_list, (25,35)))

    # plt.scatter([x for x in range(1,len(ratios1)+1)],ratios1, label='Pseudoword take1')
    # plt.xticks([x for x in range(1,len(ratios1)+1)])
    # # plt.axhline(1, color='orange', label='baseline')
    #