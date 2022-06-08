% Constants
R = 0.06;
A = pi*R.^2;
T = 0.008;
e0 = 8.85*10.^(-12); % matlab constant

F = dataa1000mgn0gd1w0(:,2); %Frequency

%Real impedance
ZR0 = dataa1000mgn0gd1w0(:,3);
ZR1 = dataa1400mgn0gd1w0(:,3);
ZR2 = dataa1800mgn0gd1w0(:,3);
ZR3 = dataa2200mgn0gd1w0(:,3);
ZR4 = dataa2600mgn0gd1w0(:,3);
ZR5 = dataa3000mgn0gd1w0(:,3);

%Imaginary impedance
ZI0 = dataa1000mgn0gd1w0(:,4);
ZI1 = dataa1400mgn0gd1w0(:,4);
ZI2 = dataa1800mgn0gd1w0(:,4);
ZI3 = dataa2200mgn0gd1w0(:,4);
ZI4 = dataa2600mgn0gd1w0(:,4);
ZI5 = dataa3000mgn0gd1w0(:,4);

%conductivity
for i = 1:61
    conduc0(i) = T/(ZR0(i)*A);
    conduc1(i) = T/(ZR1(i)*A);
    conduc2(i) = T/(ZR2(i)*A);
    conduc3(i) = T/(ZR3(i)*A);
    conduc4(i) = T/(ZR4(i)*A);
    conduc5(i) = T/(ZR5(i)*A);
end

%relative permittivitiy
for i = 1:61
    C0(i) = 1/(2*pi*F(i)*ZI0(i));
    P0(i) = (C0(i)*T)/(A*e0);

    C1(i) = 1/(2*pi*F(i)*ZI1(i));
    P1(i) = (C1(i)*T)/(A*e0);

    C2(i) = 1/(2*pi*F(i)*ZI2(i));
    P2(i) = (C2(i)*T)/(A*e0);

    C3(i) = 1/(2*pi*F(i)*ZI3(i));
    P3(i) = (C3(i)*T)/(A*e0);

    C4(i) = 1/(2*pi*F(i)*ZI4(i));
    P4(i) = (C4(i)*T)/(A*e0);

    C5(i) = 1/(2*pi*F(i)*ZI5(i));
    P5(i) = (C5(i)*T)/(A*e0);
end

figure
subplot(2,1,1)
plot(F, conduc0,'-');
hold on
plot(F, conduc1,'-');
plot(F, conduc2,'-');
plot(F, conduc3,'-');
plot(F, conduc4,'-');
plot(F, conduc5,'-');

title("Parallel plate capacitor measurement", 'interpreter',  'latex','fontsize',17);
xlabel("Frequency [Hz]", 'interpreter',  'latex','fontsize',17)
ylabel("Conductivity [S/m]", 'interpreter',  'latex','fontsize',17);

leg = legend('1', '2', '3', '4', '5', '6', 'interpreter',  'latex','fontsize',17);
title(leg,'Solution', 'interpreter',  'latex','fontsize',17);

subplot(2,1,2)
plot(F, P0,'-');
hold on
plot(F, P1,'-');
plot(F, P2,'-');
plot(F, P3,'-');
plot(F, P4,'-');
plot(F, P5,'-');

leg = legend('1', '2', '3', '4', '5', '6', 'interpreter',  'latex','fontsize',17);
title(leg, 'Solution', 'interpreter',  'latex','fontsize',17);

title("Parallel plate capacitor measurement", 'interpreter',  'latex','fontsize',17);
xlabel("Frequency [Hz]", 'interpreter',  'latex','fontsize',17);
ylabel("Permittivity [F/m]", 'interpreter',  'latex','fontsize',17);
