%% testing fft stuff
n = 1000;
t = linspace(0,2,n);
Fs = (n-1) / (t(end) - t(1));
period = 0.03;
y = sin(2*pi/period * t);
% y = t;

figure(1)
plot(t,y);

Y = fftshift(fft(y, 5000));
N = length(Y);
f = linspace(-Fs/2, Fs/2, N);

Yf = bandpass(Y, [1, 50], Fs);


figure(2)
hold on;
plot(f, abs(Y));
plot(f, abs(Yf));
hold off;