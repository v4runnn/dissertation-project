% Sampling frequency
Fs = 1e6;           % 1 MHz (your testbench sim Fs)

% Filter design: 2nd-order bandpass at 30 kHz, Q ≈ 3
f0 = 30e3;          % centre frequency
Q = 3;              % quality factor
w0 = 2*pi*f0/Fs;    % normalised angular frequency

alpha = sin(w0)/(2*Q);

b0 =  alpha;
b1 =  0;
b2 = -alpha;
a0 =  1 + alpha;
a1 = -2*cos(w0);
a2 =  1 - alpha;

% Normalise so a0 = 1
b = [b0 b1 b2]/a0;
a = [1 a1/a0 a2/a0];

% Frequency response
[H,f] = freqz(b,a,1024,Fs);

% Plot
figure;
plot(f/1000, 20*log10(abs(H)),'LineWidth',1.5);
xlabel('Frequency (kHz)');
ylabel('Magnitude (dB)');
title('Magnitude Response of Designed Band-pass Filter');
grid on;
xlim([0 100]);  % zoom into 0–100 kHz