% Constants
R = 0.06;
A = pi*R.^2;
T = 0.008;
e0 = 8.85*10.^(-12); % matlab constant

F = dataa3000mgn1000mg(:,2); %Frequency
colors = ["magenta", "red", "green", "yellow", "blue", "cyan"];

%-----conductivity
Reals = [dataa3000mgn750mgd2w12g(:,3) dataa3000mgn1500mgd2w12g(:,3) dataa3000mgn1750mgd3w0(:,3)];
Realsd2 = [dataa3000mgn750mgd2w60g(:,3) dataa3000mgn1500mgd2w60g(:,3) dataa3000mgn1750mgd3w60g(:,3)];
Realsd3 = [dataa3000mgn750mgd2w120g(:,3) dataa3000mgn1500mgd2w120g(:,3) dataa3000mgn1750mgd3w120g(:,3)];

conductivity_d1 = (Reals .^(-1)) * (T/A);
conductivity_d2 = (Realsd2 .^(-1)) * (T/A);
conductivity_d3 = (Realsd3 .^(-1)) * (T/A);

figure
subplot(1,2,1)
hold on
for i = 1:size(conductivity_d1,2)
   p1 = semilogy(F, conductivity_d1(:,i), '-', 'LineWidth', 1.5);   
   p2 = semilogy(F, conductivity_d2(:,i), '--', 'LineWidth', 1.5);  
   p3 = semilogy(F, conductivity_d3(:,i), ':', 'LineWidth', 1.5);  
   p1.Color = colors(i);
   p2.Color = colors(i);
   p3.Color = colors(i); 
end
hold off

title("Pressure measurement", 'interpreter',  'latex','fontsize',17);
xlabel("Frequency [Hz]", 'interpreter',  'latex','fontsize',17)
ylabel("Conductivity [S/m]", 'interpreter',  'latex','fontsize',17);

leg = legend('8','','', '11','','', '12','interpreter',  'latex','fontsize',13,'Location','northwest');
title(leg,'Solution', 'interpreter',  'latex','fontsize',13);

%-----relative permittivitiy

Imagsd1 = [dataa3000mgn750mgd2w12g(:,4) dataa3000mgn1500mgd2w12g(:,4) dataa3000mgn1750mgd3w0(:,4)];
Imagsd2 = [dataa3000mgn750mgd2w60g(:,4) dataa3000mgn1500mgd2w60g(:,4) dataa3000mgn1750mgd3w60g(:,4)];
Imagsd3 = [dataa3000mgn750mgd2w120g(:,4) dataa3000mgn1500mgd2w120g(:,4) dataa3000mgn1750mgd3w120g(:,4)];

F_part = (F .^-1) * (1/(2*pi));

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
   f1 = semilogy(F, permittivity1(:,k), '-', 'LineWidth', 1.5);
   f2 = semilogy(F, permittivity2(:,k), '--', 'LineWidth', 1.5);
   f3 = semilogy(F, permittivity3(:,k), ':', 'LineWidth', 1.5);
   f1.Color = colors(k);
   f2.Color = colors(k);
   f3.Color = colors(k);
end
hold off

leg = legend('8','','', '11','','', '12', 'interpreter',  'latex','fontsize',13);
title(leg, 'Solution', 'interpreter',  'latex','fontsize',13);

title("Pressure measurement", 'interpreter',  'latex','fontsize',17);
xlabel("Frequency [Hz]", 'interpreter',  'latex','fontsize',17);
ylabel("Permittivity [F/m]", 'interpreter',  'latex','fontsize',17);
