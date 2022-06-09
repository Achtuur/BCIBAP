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
subplot(1,2,1)
plot(F, conduc1,'-');
hold on
plot(F, conduc2,'-');
plot(F, conduc3,'-');
plot(F, conduc4,'-');
plot(F, conduc5,'-');
plot(F, conduc6,'-');

title("Parallel plate capacitor measurement", 'interpreter',  'latex','fontsize',17);
xlabel("Frequency [Hz]", 'interpreter',  'latex','fontsize',17)
%xlabel("Frequency [Hz]");
ylabel("Conductivity [S/m]", 'interpreter',  'latex','fontsize',17);

leg = legend('7', '8', '9', '10', '11', '12', 'interpreter',  'latex','fontsize',12);
title(leg,'Solution', 'interpreter',  'latex','fontsize',12);

subplot(1,2,2)
plot(F, P1,'-');
hold on
plot(F, P2,'-');
plot(F, P3,'-');
plot(F, P4,'-');
plot(F, P5,'-');
plot(F, P6,'-');

leg = legend('7', '8', '9', '10', '11', '12', 'interpreter',  'latex','fontsize',12);
title(leg, 'Solution', 'interpreter',  'latex','fontsize',12);

title("Parallel plate capacitor measurement", 'interpreter',  'latex','fontsize',17);
xlabel("Frequency [Hz]", 'interpreter',  'latex','fontsize',17);
ylabel("Permittivity [F/m]", 'interpreter',  'latex','fontsize',17);

%set(gca, 'YScale', 'log')


