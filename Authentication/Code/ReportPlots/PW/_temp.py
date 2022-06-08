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
from FeaturesLos import left_hemisphere_difference_ratio

if __name__ == '__main__':
    scores = []
    for i in range(1,6):
        INTERVAL = i
        data = np.load(Path('../../Data/ExperimentResults/recorded_data/recordings_numpy/Joos/OpenBCISession_Joos_exp_pseudo2_1s_take1.npy'))
        data_filtered = PreprocessingPipeline(data).start()
        data_cropped = crop(data_filtered, 2, 250)
        data_cropped = list(map(lambda x: Filter.remove_bad_channels(x), data_cropped))
        data_cropped = [x for x in data_cropped if x is not None]
        data_to_analyse = np.concatenate(data_cropped)

        data_words = data_to_analyse[:20*250,:]
        data_pw_words = data_to_analyse[20*250:,:]
        data_words_list = crop(data_words, INTERVAL, 250)
        data_pw_list = crop(data_pw_words, INTERVAL, 250)

        ratios1 = []

        for pw_data_point in data_pw_list:
            ratios1.append(left_hemisphere_difference_ratio(pw_data_point, data_words_list, (25,35)))

        # plt.scatter([x for x in range(1,len(ratios1)+1)],ratios1, label='Pseudoword take1')
        # plt.xticks([x for x in range(1,len(ratios1)+1)])
        # plt.axhline(1, color='orange', label='baseline')

        data = np.load(Path('../../Data/ExperimentResults/recorded_data/recordings_numpy/Joos/OpenBCISession_Joos_exp_pseudo2_1s_take2.npy'))
        data_filtered = PreprocessingPipeline(data).start()
        data_cropped = crop(data_filtered, 2, 250)
        data_cropped = list(map(lambda x: Filter.remove_bad_channels(x), data_cropped))
        data_cropped = [x for x in data_cropped if x is not None]
        data_to_analyse = np.concatenate(data_cropped)

        data_words = data_to_analyse[:20*250,:]
        data_pw_words = data_to_analyse[20*250:,:]
        data_words_list = crop(data_words, INTERVAL, 250)
        data_pw_list = crop(data_pw_words, INTERVAL, 250)

        ratios2 = []

        for pw_data_point in data_pw_list:
            ratios2.append(left_hemisphere_difference_ratio(pw_data_point, data_words_list, (25,35)))

        # plt.scatter([x for x in range(1,len(ratios2)+1)],ratios2, label='Pseudoword take2')
        # plt.xticks([x for x in range(1,len(ratios2)+1)])
        # plt.axhline(1, color='orange', label='baseline')
        # plt.show(block=True)

        data = np.load(Path('../../Data/ExperimentResults/recorded_data/recordings_numpy/Joos/OpenBCISession_Joos_exp_pseudo2_1s_take3.npy'))
        data_filtered = PreprocessingPipeline(data).start()
        data_cropped = crop(data_filtered, 2, 250)
        data_cropped = list(map(lambda x: Filter.remove_bad_channels(x), data_cropped))
        data_cropped = [x for x in data_cropped if x is not None]
        data_to_analyse = np.concatenate(data_cropped)

        data_words = data_to_analyse[:20*250,:]
        data_pw_words = data_to_analyse[20*250:,:]
        data_words_list = crop(data_words, INTERVAL, 250)
        data_pw_list = crop(data_pw_words, INTERVAL, 250)

        ratios3 = []

        for pw_data_point in data_pw_list:
            ratios3.append(left_hemisphere_difference_ratio(pw_data_point, data_words_list, (25,35)))

        ratios = []
        for ratio in ratios1:
            ratios.append(ratio)
        for ratio in ratios2:
            ratios.append(ratio)
        for ratio in ratios3:
            ratios.append(ratio)
    
        total = len(ratios)
        higher = 0
        for ratio in ratios:
            if ratio <= 1:
                higher += 1
    
        score = higher/total
        scores.append(score)
        # plt.scatter([x for x in range(1,len(ratios3)+1)],ratios3, label='Pseudoword take3')
        # plt.xticks([x for x in range(1,len(ratios3)+1)])
        # plt.axhline(1, color='orange', label='baseline')
        # plt.title(f'Score: {score}')
        # plt.show(block=True)
    plt.bar([1,2,3,4,5] ,scores)
    plt.title('Feature prediction score for different measurement intervals', fontsize=16)
    plt.xlabel('Measurement Interval [s]', fontsize=16)
    plt.ylabel('Score [%]', fontsize=16)
    plt.show(block=True)

        








