% Constants
R = 0.06;
A = pi*R.^2;
T = 0.008;
e0 =  8.854187817*10.^(-12);

%Frequency Array
F = dataa3000mgn1000mg(:,2); 

%TU-Delft colors
colorshex = ["#0300a6","#fa7029","#00d999","#84f0e1","#c8c942","#a700cf","#fa7029","#ebed5c","#75ffad","#0300a6","#00d999"];

% ---Resistance
Reals = [dataa3000mgn750mgd2w12g(:,3) dataa3000mgn1500mgd2w12g(:,3) dataa3000mgn1750mgd3w0(:,3)];
Realsd2 = [dataa3000mgn750mgd2w60g(:,3) dataa3000mgn1500mgd2w60g(:,3) dataa3000mgn1750mgd3w60g(:,3)];
Realsd3 = [dataa3000mgn750mgd2w120g(:,3) dataa3000mgn1500mgd2w120g(:,3) dataa3000mgn1750mgd3w120g(:,3)];

% conductivity
conductivity_d1 = (Reals .^(-1)) * (T/A);
conductivity_d2 = (Realsd2 .^(-1)) * (T/A);
conductivity_d3 = (Realsd3 .^(-1)) * (T/A);

figure
subplot(1,2,1)
hold on
for i = 1:size(conductivity_d1,2)
   %logarithmic y-axis
   p1 = semilogy(F, conductivity_d1(:,i), '-', 'LineWidth', 1.5);   
   p2 = semilogy(F, conductivity_d2(:,i), '--', 'LineWidth', 1.5);  
   p3 = semilogy(F, conductivity_d3(:,i), ':', 'LineWidth', 1.5);  
   p1.Color = colorshex(i);
   p2.Color = colorshex(i);
   p3.Color = colorshex(i); 
end
hold off
box on

%Style
title("Pressure measurement", 'interpreter',  'latex','fontsize',18);
xlabel("Frequency [Hz]", 'interpreter',  'latex','fontsize',18)
ylabel("Conductivity [S/m]", 'interpreter',  'latex','fontsize',18);
leg = legend('8','','', '11','','', '12','interpreter',  'latex','fontsize',14,'Location','northwest');
title(leg,'Solution', 'interpreter',  'latex','fontsize',14);

% ---Reactance
Imagsd1 = [dataa3000mgn750mgd2w12g(:,4) dataa3000mgn1500mgd2w12g(:,4) dataa3000mgn1750mgd3w0(:,4)];
Imagsd2 = [dataa3000mgn750mgd2w60g(:,4) dataa3000mgn1500mgd2w60g(:,4) dataa3000mgn1750mgd3w60g(:,4)];
Imagsd3 = [dataa3000mgn750mgd2w120g(:,4) dataa3000mgn1500mgd2w120g(:,4) dataa3000mgn1750mgd3w120g(:,4)];

F_part = (F .^-1) * (1/(2*pi));

% Permittivity from capacitance
for j = 1:size(Imagsd1,2)        
    C1 = F_part .* (Imagsd1(:,j) .^ -1);
    permittivity1(:,j) = C1 .* (T/(A*e0));
    
    C2 = F_part .* (Imagsd2(:,j) .^ -1);
    permittivity2(:,j) = C2 .* (T/(A*e0));
    
    C3 = F_part .* (Imagsd3(:,j) .^ -1);
    permittivity3(:,j) = C3 .* (T/(A*e0));
end

subplot(1,2,2)
hold on
for k = 1:size(permittivity1,2)
   %logarithmic y-axis
   f1 = semilogy(F, permittivity1(:,k), '-', 'LineWidth', 1.5);
   f2 = semilogy(F, permittivity2(:,k), '--', 'LineWidth', 1.5);
   f3 = semilogy(F, permittivity3(:,k), ':', 'LineWidth', 1.5);
   f1.Color = colorshex(k);
   f2.Color = colorshex(k);
   f3.Color = colorshex(k);
end
hold off
box on

%Style
title("Pressure measurement", 'interpreter',  'latex','fontsize',18);
xlabel("Frequency [Hz]", 'interpreter',  'latex','fontsize',18);
ylabel("Permittivity [F/m]", 'interpreter',  'latex','fontsize',18);
leg = legend('8','','', '11','','', '12', 'interpreter',  'latex','fontsize',14);
title(leg, 'Solution', 'interpreter',  'latex','fontsize',14);