% Constants
R = 0.06;
A = pi*R.^2;
T = 0.008;
e0 = 8.85*10.^(-12); % matlab constant

F = dataa3gn750mgd2w12g(:,2); %Frequency

%Real impedance
ZR0 = dataa3gn1500mgd2(:,3); 
ZR1 = dataa3gn750mgd2w12g(:,3); 
ZR2 = dataa3gn750mgd2w60g(:,3); 
ZR3 = dataa3gn750mgd2w120g(:,3); 
ZR4 = dataa3gn1500mgd2w12g(:,3); 
ZR5 = dataa3gn1500mgd2w60g(:,3); 
ZR6 = dataa3gn1500mgd2w120g(:,3); 

%Imaginary impedance
ZI0 = dataa3gn1500mgd2(:,4); 
ZI1 = dataa3gn750mgd2w12g(:,4); 
ZI2 = dataa3gn750mgd2w60g(:,4); 
ZI3 = dataa3gn750mgd2w120g(:,4); 
ZI4 = dataa3gn1500mgd2w12g(:,4); 
ZI5 = dataa3gn1500mgd2w60g(:,4); 
ZI6 = dataa3gn1500mgd2w120g(:,4); 

%conductivity
for i = 1:61
    conduc0(i) = T/(ZR0(i)*A);
    conduc1(i) = T/(ZR1(i)*A);
    conduc2(i) = T/(ZR2(i)*A);
    conduc3(i) = T/(ZR3(i)*A);
    conduc4(i) = T/(ZR4(i)*A);
    conduc5(i) = T/(ZR5(i)*A);
    conduc6(i) = T/(ZR6(i)*A);
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
    
    C6(i) = 1/(2*pi*F(i)*ZI6(i));
    P6(i) = (C6(i)*T)/(A*e0);
end

figure

plot(F, conduc0,'--xb');
hold on
plot(F, conduc1,'--xr');
plot(F, conduc2,'--or');
plot(F, conduc3,'--.r');
plot(F, conduc4,'--xg');
plot(F, conduc5,'--og');
plot(F, conduc6,'--.g');

title("Dielectric measurement, 3g agar, day 2");
xlabel("Frequency [Hz]");
ylabel("Conductivity [S/m]");

leg = legend('0g','12g', '60g', '120g', '12g', '60g', '120g');
title(leg,'Pressure');

figure

plot(F, P0,'--xb');
hold on
plot(F, P1,'--xr');
plot(F, P2,'--or');
plot(F, P3,'--.r');
plot(F, P4,'--xg');
plot(F, P5,'--og');
plot(F, P6,'--.g');

leg = legend('0g','12g', '60g', '120g', '12g', '60g', '120g');
title(leg,'Pressure');

title("Dielectric measurement, 3g agar");
xlabel("Frequency [Hz]");
ylabel("Permittivity [F/m]");

%set(gca, 'YScale', 'log')


