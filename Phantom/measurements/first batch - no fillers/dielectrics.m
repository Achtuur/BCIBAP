% Constants
R = 0.06;
A = pi*R.^2;
T = 0.008;
e0 = 8.85*10.^(-12);

F = data3g(:,2); %Frequency

ZR1 = data3g(:,3); %Real impedance
ZI1 = data3g(:,4); %Imaginary impedance
ZI2 = data3g0(:,4); %Imaginary impedance
ZI3 = data3g50mg(:,4); %Imaginary impedance
ZI4 = data6g(:,4); %Imaginary impedance
ZI5 = data3g15(:,4); %Imaginary impedance

for i = 1:61
    conduc1(i) = T/(ZR1(i)*A);
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
end

figure

semilogy(F, conduc1,'--ob');

title("Dielectric measurement");
xlabel("Frequency [Hz]");
ylabel("Conductivity [S/m]");

figure

semilogy(F, P1,'--xr');
hold on
semilogy(F, P2,'--xg');
semilogy(F, P3,'--xb');
semilogy(F, P4,'--xm');
semilogy(F, P5,'--xy');

legend("3G agar, 0g zout, oud", "3g agar, 0.75g zout", "3g agar, 0.5g zout", "6g agar, 0g zout, oud", "3g agar, 1.5g zout")

title("Dielectric measurement");
xlabel("Frequency [Hz]");
ylabel("Permittivity [F/m]");


