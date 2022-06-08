% Constants
R = 0.06;
A = pi*R.^2;
T = 0.008;
e0 = 8.85*10.^(-12);

F = data3g1000mg(:,2); %Frequency

%Real impedance
ZR1 = data3g500mg(:,3); 
ZR2 = data3g750mg(:,3); 
ZR3 = data3g1000mg(:,3); 
ZR4 = data3g1250mg(:,3); 
ZR5 = data3g1500mg(:,3); 
ZR6 = data3g1750mg(:,3); 

ZI1 = data3g500mg(:,4); 
ZI2 = data3g750mg(:,4); 
ZI3 = data3g1000mg(:,4); 
ZI4 = data3g1250mg(:,4); 
ZI5 = data3g1500mg(:,4); 
ZI6 = data3g1750mg(:,4); 

for i = 1:61
    conduc1(i) = T/(ZR1(i)*A);
    conduc2(i) = T/(ZR2(i)*A);
    conduc3(i) = T/(ZR3(i)*A);
    conduc4(i) = T/(ZR4(i)*A);
    conduc5(i) = T/(ZR5(i)*A);
    conduc6(i) = T/(ZR6(i)*A);
end

for i = 1:61
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

plot(F, conduc1,'--ob');
hold on
plot(F, conduc2,'--or');
plot(F, conduc3,'--oy');
plot(F, conduc4,'--om');
plot(F, conduc5,'--og');
plot(F, conduc6,'--oc');

title("Dielectric measurement");
xlabel("Frequency [Hz]");
ylabel("Conductivity [S/m]");

leg = legend('500 mg', '750 mg', '1000 mg', '1250 mg', '1500 mg', '1750 mg');
title(leg,'Salt concentrations');

figure

plot(F, P1,'--xr');
hold on
plot(F, P2,'--xg');
plot(F, P3,'--xb');
plot(F, P4,'--xm');
plot(F, P5,'--xy');
plot(F, P6,'--xc');

leg = legend('500 mg', '750 mg', '1000 mg', '1250 mg', '1500 mg', '1750 mg');
title(leg, 'Salt concentrations');

title("Dielectric measurement, 3g agar");
xlabel("Frequency [Hz]");
ylabel("Permittivity [F/m]");

%set(gca, 'YScale', 'log')


