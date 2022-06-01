clear;
close all;
clc;
%% testing fft stuff
n = 1000;
t = linspace(0,2,n);
Fs = (n-1) / (t(end) - t(1));
period = 0.5;
y1 = sin(2*pi/period * t);
y2 = sin(2*pi/period*5 * t);
% y = t;

figure(1)
hold on;
plot(t,y1);
plot(t, y2);
hold off;

Y1 = fftshift(fft(y1, 5000));
Y2 = fftshift(fft(y2, 5000));
N = length(Y1);
f = linspace(-Fs/2, Fs/2, N);


figure(2)
hold on;
plot(f, abs(Y1));
plot(f, abs(Y2));
hold off;

xlim([0, 15]);