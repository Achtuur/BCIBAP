import sys
import platform
from pathlib import Path 
import numpy as np
if platform.system() == "Windows":
    sys.path.append(str(Path('PipelineComponents/Preprocessing').resolve()))
    sys.path.append(str(Path('PipelineComponents/FeatureExtraction').resolve()))
    sys.path.append(str(Path('Data/ExperimentResults').resolve()))
    sys.path.append(str(Path('Data').resolve()))
    sys.path.append(str(Path('PipelineComponents/Classification').resolve()))
else:
    sys.path.append(str(Path('./PipelineComponents/Preprocessing').resolve()))
    sys.path.append(str(Path('./PipelineComponents/FeatureExtraction').resolve()))
    sys.path.append(str(Path('./PipelineComponents/Classification').resolve()))
    sys.path.append(str(Path('./Data').resolve()))
    sys.path.append(str(Path('./Data/ExperimentResults').resolve()))
from ExperimentWrapper import ExperimentWrapper
from PreprocessingPipeline import PreprocessingPipeline
from FeaturePipeline import FeaturePipeline
from crop import crop
from crop import cut
import scipy.signal as sig
from Filters import Filter
import matplotlib.pyplot as plt
from statistics import mean

def ft_classification1(data, labels, t_cutoff = 500, channel = 0, f_tag = 15, f_band = 2):
    data = np.transpose(data)
    f_low = f_tag - f_band
    print(f_low)
    f_high = f_tag + f_band
    print(f_high)
    nonfiltered_fft1 = np.abs(np.fft.fft(data[:500])[:250])
    nonfiltered_fft2 = np.abs(np.fft.fft(data[500:1000])[:250])
    data_bandpass = Filter.band_pass_filter(data, 3, (f_low,f_high), 250)
    data_bandstop = Filter.band_stop_filter(data, 3, (f_low,f_high), 250)
    split_bandpass = cut(data_bandpass, t_window = 2)
    fft_bandpass1 = np.abs(np.fft.fft(split_bandpass[0])[:250])
    fft_bandpass2 = np.abs(np.fft.fft(split_bandpass[1])[:250])
    split_bandstop = cut(data_bandstop, t_window = 2)
    fft_bandstop1 = np.abs(np.fft.fft(split_bandstop[0])[:250])
    fft_bandstop2 = np.abs(np.fft.fft(split_bandstop[1])[:250])
    x = np.linspace(0,125,250)
    plt.plot(x,nonfiltered_fft1, label = 'No filter')
    plt.plot(x,fft_bandpass1, label = 'Bandpass filter')
    plt.plot(x,fft_bandstop1, label = 'Bandstop filter')
    plt.xlim([0, 40])
    plt.title('FFT for a 2 second time window without flashing')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude [\u03BCV]')
    plt.legend(frameon = True)
    plt.xlim([0, 40])
    plt.show(block = True)
    plt.plot(x,nonfiltered_fft2, label = 'No filter')
    plt.plot(x,fft_bandpass2, label = 'Bandpass filter')
    plt.plot(x,fft_bandstop2, label = 'Bandstop filter')
    plt.title('FFT for a 2 second time window with flashing')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude [\u03BCV]')
    plt.legend(frameon = True)
    plt.xlim([0, 40])
    plt.show(block = True)
    mean_pass = []
    mean_stop = []
    ratio = []
    for data_window in split_bandpass:
        mean_pass.append(np.mean(np.square(data_window[:t_cutoff])))
    for index, data_window in enumerate(split_bandstop):
        mean_stop.append(np.mean(np.square(data_window[:t_cutoff])))
        ratio.append(mean_pass[index] / mean_stop[index])

    passband_flashes = mean_pass[1::2]
    passband_control = mean_pass[::2]
    flashes = ratio[1::2]
    control = ratio[::2]

    return flashes, control, passband_flashes, passband_control

def ft_classification2(data, labels, t_cutoff = 400, channel = 0, offset = 200):
    data = np.transpose(data)
    data_bandpass = Filter.band_pass_filter(data, 3, (13,17), 250)
    data_bandstop = Filter.band_stop_filter(data, 3, (13,17), 250)
    split_bandpass_offset = cut(data_bandpass, t_window = 2, offset = offset)
    split_bandstop_offset = cut(data_bandstop, t_window = 2, offset = offset)
    bandpass_flashes = split_bandpass_offset[::2]
    bandstop_flashes = split_bandstop_offset[::2]
    split_bandpass = cut(data_bandpass, t_window = 2, offset = 0)
    split_bandstop = cut(data_bandstop, t_window = 2, offset = 0)
    bandpass_control = split_bandpass[::2]
    bandstop_control = split_bandstop[::2]

    diff_flashes = []
    diff_control = []
    #control group
    for index, data_window in enumerate(bandpass_flashes):
        power_ratio_before = np.mean(np.square(data_window[:offset])) #/ np.mean(np.square(bandstop_flashes[index][:offset]))
        power_ratio_after = np.mean(np.square(data_window[offset:t_cutoff])) #/ np.mean(np.square(bandstop_flashes[index][offset:t_cutoff]))
        diff_flashes.append(power_ratio_after - power_ratio_before)

    for index, data_window in enumerate(bandpass_control):
        power_ratio_before = np.mean(np.square(data_window[:offset])) #/ np.mean(np.square(bandstop_control[index][:offset])) 
        power_ratio_after = np.mean(np.square(data_window[offset:t_cutoff])) #/ np.mean(np.square(bandstop_control[index][offset:t_cutoff]))
        diff_control.append(power_ratio_after - power_ratio_before)
        

    return diff_flashes, diff_control

def ft_classification4(data, t_cutoff = 2, channel = 7, f_sampling = 250, f_tagging = 15):
    data = np.transpose(data)
    data = data[channel]
    data = cut(data, t_window = 2)

    w = 2  * np.pi * f_tagging / f_sampling
    N = t_cutoff * f_sampling
    time = np.arange(0, N, 1)
    amplitude = np.sin( w * time)

    for data_window in data:
        phase = hilphase(data, amplitude)
        print(np.mean(phase))

    return

def hilphase(y1,y2):
    sig1_hill=sig.hilbert(y1)
    sig2_hill=sig.hilbert(y2)
    pdt=(np.inner(sig1_hill,np.conj(sig2_hill))/(np.sqrt(np.inner(sig1_hill,
            np.conj(sig1_hill))*np.inner(sig2_hill,np.conj(sig2_hill)))))
    phase = np.angle(pdt)

    return phase
    

    


from statistics import mean
if __name__ == "__main__":

    EXPERIMENTS = []

    # EXPERIMENT_SIMON_6HZ = ExperimentWrapper("Simon", "ft")
    # EXPERIMENT_SIMON_6HZ.set_experiment_data(Path(".\Data\ExperimentResults\\recorded_data\\recordings_numpy\\Simon\OpenBCISession_Simon_stage1_6hz.npy"))
    # EXPERIMENT_SIMON_6HZ.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/simon_23-05-2022_ft1_take2.csv"))
    # EXPERIMENTS.append(EXPERIMENT_SIMON_6HZ)

    EXPERIMENT_SIMON_TAKE_1 = ExperimentWrapper("Simon", "ft")
    EXPERIMENT_SIMON_TAKE_1.set_experiment_data(Path(".\Data\ExperimentResults\\recorded_data\\recordings_numpy\\Simon\OpenBCISession_Simon_stage1_take1.npy"))
    EXPERIMENT_SIMON_TAKE_1.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/simon_23-05-2022_ft1_take1.csv"))
    EXPERIMENTS.append(EXPERIMENT_SIMON_TAKE_1)

    EXPERIMENT_SIMON_TAKE_2 = ExperimentWrapper("Simon", "ft")
    EXPERIMENT_SIMON_TAKE_2.set_experiment_data(Path(".\Data\ExperimentResults\\recorded_data\\recordings_numpy\\Simon\OpenBCISession_Simon_stage1_take2.npy"))
    EXPERIMENT_SIMON_TAKE_2.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/simon_23-05-2022_ft1_take2.csv"))
    EXPERIMENTS.append(EXPERIMENT_SIMON_TAKE_2)

    EXPERIMENT_SAM_TAKE_1 = ExperimentWrapper("Sam", "ft")
    EXPERIMENT_SAM_TAKE_1.set_experiment_data(Path(".\Data\ExperimentResults\\recorded_data\\recordings_numpy\\Sam\OpenBCISession_Sam_stage1_take1.npy"))
    EXPERIMENT_SAM_TAKE_1.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/Sam_23-05-2022_ft1_take1.csv"))
    EXPERIMENTS.append(EXPERIMENT_SAM_TAKE_1)

    EXPERIMENT_SAM_TAKE_2 = ExperimentWrapper("Sam", "ft")
    EXPERIMENT_SAM_TAKE_2.set_experiment_data(Path(".\Data\ExperimentResults\\recorded_data\\recordings_numpy\\Sam\OpenBCISession_Sam_stage1_take2.npy"))
    EXPERIMENT_SAM_TAKE_2.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/Sam_23-05-2022_ft1_take2.csv"))
    EXPERIMENTS.append(EXPERIMENT_SAM_TAKE_2)

    EXPERIMENT_JOOS_TAKE_1 = ExperimentWrapper("Joos", "ft")
    EXPERIMENT_JOOS_TAKE_1.set_experiment_data(Path(".\Data\ExperimentResults\\recorded_data\\recordings_numpy\\Joos\OpenBCISession_Joos_stage1_take1.npy"))
    EXPERIMENT_JOOS_TAKE_1.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/Sam_23-05-2022_ft1_take1.csv"))
    EXPERIMENTS.append(EXPERIMENT_JOOS_TAKE_1)

    EXPERIMENT_JOOS_TAKE_2 = ExperimentWrapper("Joos", "ft")
    EXPERIMENT_JOOS_TAKE_2.set_experiment_data(Path(".\Data\ExperimentResults\\recorded_data\\recordings_numpy\\Joos\OpenBCISession_Joos_stage1_take2.npy"))
    EXPERIMENT_JOOS_TAKE_2.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/Sam_23-05-2022_ft1_take2.csv"))
    EXPERIMENTS.append(EXPERIMENT_JOOS_TAKE_2)

    
    all_flashes = []
    all_control = []
    plots = 0

    subplots = False
    truthtable = True
    test = '1'

    if subplots:
        fig, axs = plt.subplots(2,2)
    
    boundary = []
    all_matrixes = []

    for experiment in EXPERIMENTS:
        print(experiment)
        # print(experiment.get_subject())
        # print(experiment.get_experiment_description_file())
        data = PreprocessingPipeline(experiment.get_experiment_data()).start()
        data = Filter.remove_bad_channels(data)
        #Take average of channels
        av_channels = []
        for sample in data:
            av_channels.append(mean(sample))
        data = av_channels


        labels = [] #add in labels later, for step 1 it is not necessary

        plotx = plots % 2
        ploty = int(plots/2)
        plots = plots + 1

        if subplots:
            if plots == 2:
                break

        flashes_matrix = []
        control_matrix = []
        if test == '1':    
            diff = []
            freq = []

            flashes, control, passband_flashes, passband_control = ft_classification1(data, labels, t_cutoff = 250, channel = 7, f_band = 2)


            #power scatter plot######################################################
            # flashes, control, passband_flashes, passband_control = ft_classification1(data, labels, t_cutoff = 250)
            # x = np.linspace(0, len(flashes), len(flashes))
            # pb_av_flash = [mean(passband_flashes)] * len(x)
            # pb_av_control = [mean(passband_control)] * len(x)
            # flash_av = [mean(flashes)] * len(x)
            # control_av = [mean(control)] * len(x)

            
            # axs[plotx,ploty].scatter(x, flashes, label = 'flashes')
            # axs[plotx,ploty].scatter(x, control, label = 'control')
            # axs[plotx,ploty].plot(x, flash_av, label = 'average flashes')
            # axs[plotx,ploty].plot(x, control_av, label = 'average control')
            ############################################################################

            #axs.set(xlabel = 'samples', ylabel = 'power')
            ####################################################################

            #test for optimal bandpass length ##################################
            # diff = []
            # for i in range(500):
            #     f_band = i * 0.01
            #     flashes, control = ft_classification1(data, labels, t_cutoff = 500, channel = 7, f_band = f_band)
            #     diff.append(mean(flashes) -mean(control))
            # x = np.linspace(0, len(diff) * 0.02, len(diff))
            # plt.xlabel('distance between bandpass and stopband cutoff frequencies (Hertz)')
            # plt.ylabel('Power difference between average of flash and control samples(V^2')
            # plt.plot(x, diff)
            ###################################################################

        elif test == '2':
            flashes, control = ft_classification2(data, labels, t_cutoff = 500, offset = 250, channel = 5)

            flashes_mean = [np.mean(flashes)] * 20
            control_mean = [np.mean(control)] * 20
            x = np.linspace(0,20,20)
            axs[plotx,ploty].scatter(x, flashes, label = 'flashes')
            axs[plotx,ploty].scatter(x, control, label = 'control')
            axs[plotx,ploty].plot(x, flashes_mean, label = 'flash mean')
            axs[plotx,ploty].plot(x, control_mean, label = 'control mean')


            # plt.bar(x, flashes)
            # plt.show(block = True)


        elif test == '3':
            P_flashes = np.zeros(20)
            P_control = np.zeros(20)
            for i in range(1,4):
                flashes, control, passband_flashes, passband_control = ft_classification1(data, labels, t_cutoff = 250, channel = 0, f_tag =  15*0.5*i, f_band = 0.3)
                P_flashes = np.add(np.array(flashes), P_flashes)
                P_control = np.add(np.array(control), P_control)
            all_flashes.append(P_flashes)
            all_control.append(P_control)
            if subplots:
                flashes_mean = [np.mean(P_flashes)] * 20
                control_mean = [np.mean(P_control)] * 20
                x = np.linspace(0,20,20)
                axs[plotx,ploty].scatter(x, P_flashes, label = 'flashes')
                axs[plotx,ploty].scatter(x, P_control, label = 'control')
                axs[plotx,ploty].plot(x, flashes_mean, label = 'flash mean')
                axs[plotx,ploty].plot(x, control_mean, label = 'control mean')

            boundary.append((np.mean(P_flashes) + np.mean(P_control)) / 2)


            


        elif test == '4':
            ft_classification4(data)
        # Set the figure size
        # plt.rcParams["figure.figsize"] = [7.00, 3.50]
        # plt.rcParams["figure.autolayout"] = True
        # plt.bar(range(0,40), ratio)

        # Display the plot
        #plt.show()   
        # 
#This is for subplots#################################### 
    if subplots:
        x_values = [''] * 20
        x_values[19] = 20 
        x_values[0] = 0
        #Used for multiple subplots
        axs[0,1].legend(loc  = 'upper right', frameon = True)
        axs[0,0].set_title('Power difference before and after 1 second for M1')
        fig.text(0.085, 0.5, 'Power difference [\u03BCV^2]', va='center', rotation='vertical')
        fig.text(0.5, 0.04, '2 second data windows', ha='center')
        axs[1,0].set_xticks(x, x_values)
        axs[0,0].set_xticks(x, x_values)
        axs[0,1].set_xticks(x, x_values)
        axs[1,1].set_xticks(x, x_values)
        axs[0,1].set_title('Power difference before and after 1 second for M2')
        plt.show(block = True)

    boundary = mean(boundary)
    all_flashes = [item for sublist in all_flashes for item in sublist]
    all_control = [item for sublist in all_control for item in sublist]

    if truthtable:
        tp = 0
        tn = 0
        fp = 0
        fn = 0

        for flash in all_flashes:
            if flash >= boundary:
                tp = tp + 1
            else:
                fp = fp + 1
        
        for control in all_control:
            if control < boundary:
                tn = tn + 1
            else:
                fn = fn + 1

        print(tp / len(all_flashes))
        print(fp / len(all_flashes))
        print(tn / len(all_control))
        print(fn / len(all_control))
        print((tp + tn)/ (2 * len(all_flashes)))
        print((fn + fp)/ (2 * len(all_flashes)))

# x = np.linspace(1, len(all_data), len(all_data))
# print(all_data)
# plt.bar(x, all_data)
# plt.show(block = True)
# xvalues = np.linspace(0,10,500)
# plt.title('Power difference as a function of bandwith between cut off frequencies with 15 Hz center frequency')
# plt.ylabel('Power difference flash  samples and control samples [\u03BCV^2]')
# plt.xlabel('Bandwith [Hz]')
plt.show(block = True)
    