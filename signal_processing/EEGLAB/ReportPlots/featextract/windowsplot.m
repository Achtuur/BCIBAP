%% Show ASR using sine (doesnt really work lol)
%% init
clc; clear; close all;
eegpath = AddPath();


%% get data
Fs = 75;
L = Fs;
fac = 100;
%% x axis
fshift = linspace(-Fs/2, Fs/2, L*fac) / Fs;
%Rectangular
rect = fftshift(fft(rectwin(L), L*fac))';
rect = mag2db(abs(rect));
trunc_rect = -15;
rect(rect < trunc_rect) = trunc_rect;
%Triangular
trian = fftshift(fft(triang(L), L*fac))';
trian = mag2db(abs(trian));
trunc_trian = -55;
trian(trian < trunc_trian) = trunc_trian;
%Hanning
han = fftshift(fft(hann(L), L*fac))';
han = mag2db(abs(han));
trunc_han = -95;
han(han < trunc_han) = trunc_han;
%Hamming
ham = fftshift(fft(hamming(L), L*fac))';
ham = mag2db(abs(ham));
trunc_ham = -45;
ham(ham < trunc_ham) = trunc_ham;
%Blackman
blk = fftshift(fft(blackman(L), L*fac))';
blk = mag2db(abs(blk));
trunc_blk = -100;
blk(blk < trunc_blk) = trunc_blk;
% f = -0.3, 0.3
i = find(fshift > -0.05 & fshift < 0.05);
i2 = find(blk(i) < -50);
i2 = i(i2); %fix indices
blk(i2) = -40;
%Kaiser
kai = fftshift(fft(kaiser(L, 3), L*fac))';
kai = mag2db(abs(kai));
trunc_kai = -50;
kai(kai < trunc_kai) = trunc_kai;


%% plot

fig = figure(1);
hold on;
linestyle = '-';
ax(1) = plot(fshift, rect, linestyle); %rectangular
ax(2) = plot(fshift, trian, linestyle); %triangular
ax(3) = plot(fshift, han, linestyle); %hanning
ax(4) = plot(fshift, ham); %hamming
ax(5) = plot(fshift, blk); %Blackman
ax(6) = plot(fshift, kai); %kaiser
hold off;
plotline(ax, 1.5);
br = 45;
plotcolor(ax(1), 'green',   'colordiff', br);
plotcolor(ax(2), 'purple',  'colordiff', br);
plotcolor(ax(3), 'red',     'colordiff', br);
plotcolor(ax(4), 'orange',  'colordiff', br);
plotcolor(ax(5), 'cyan',    'colordiff', br);
plotcolor(ax(6), 'magenta', 'colordiff', br);
plottext(ax, 'Magnitude Spectrum for different types of window functions', { ...
    sprintf('Rectangular (truncated at %.1f dB)', trunc_rect), ...
    sprintf('Triangular (truncated at %.1f dB)', trunc_trian), ...
    sprintf('Hanning (truncated at %.1f dB)', trunc_han), ...
    sprintf('Hamming (truncated at %.1f dB)', trunc_ham), ...
    sprintf('Blackman (truncated at %.1f dB)', trunc_blk), ...
    sprintf('Kaiser (truncated at %.1f dB)', trunc_kai)...
    }, 'Frequency [Hz]', 'Amplitude [dB]', 'fontsize', 10, 'legendloc', 'best');
figsize(fig, 'o'); %try 's', 'm', 'b', 'o'/'r'

xt = [-1 : 0.125 : 1];
axis = gca;
axis.TickLabelInterpreter = 'latex';
axis.FontSize = 14;
xticks(xt);
ticklab = xt + " $f_s$";
ticklab(ceil(length(xt)/2)) = "0"; %set middle element to not have 'fs'
xticklabels(ticklab);

ylim([-125 50]);
xlim([-0.5 0.5]);
%% Save image
location = GetPath2Images(mfilename);
extension = "eps";
SaveImage(fig, location, mfilename, extension);
% close all;
