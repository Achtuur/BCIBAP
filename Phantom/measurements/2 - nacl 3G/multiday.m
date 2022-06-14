% Constants
R = 0.06;
A = pi*R.^2;
T = 0.008;
e0 = 8.85*10.^(-12); % matlab constant

F = dataa3000mgn1000mg(:,2); %Frequency
colorshex = ["#84f0e1","#0300a6","#fa7029","#a700cf","#00d999","#75ffad","#0300a6","#ebed5c"];

%-----conductivity
Reals = [dataa3000mgn500mg(:,3) dataa3000mgn750mg(:,3) dataa3000mgn1000mg(:,3) dataa3000mgn1250mg(:,3) dataa3000mgn1500mg(:,3) dataa3000mgn1750mg(:,3)];
Realsd2 = [dataa3000mgn500mgd2(:,3) dataa3000mgn750mgd2(:,3) dataa3000mgn1000mgd2(:,3) dataa3000mgn1250mgd2(:,3) dataa3000mgn1500mgd2(:,3) dataa3000mgn1750mgd2(:,3)];
Realsd3 = [dataa3000mgn500mgd3w0(:,3) dataa3000mgn750mgd3w0(:,3) dataa3000mgn1000mgd3w0(:,3) dataa3000mgn1250mgd3w0(:,3) dataa3000mgn1500mgd3w0(:,3) dataa3000mgn1750mgd3w0(:,3)];

conductivity_d1 = (Reals .^(-1)) * (T/A);
conductivity_d2 = (Realsd2 .^(-1)) * (T/A);
conductivity_d3 = (Realsd3 .^(-1)) * (T/A);

figure
subplot(1,2,1)
hold on
for i = 1:size(conductivity_d1,2)
    if i==2 || i==3 || i==5
       p1 = semilogy(F, conductivity_d1(:,i), '-', 'LineWidth', 1.5);   
       p2 = semilogy(F, conductivity_d2(:,i), '--', 'LineWidth', 1.5);  
       p3 = semilogy(F, conductivity_d3(:,i), ':', 'LineWidth', 1.5);  
       p1.Color = colorshex(i);
       p2.Color = colorshex(i);
       p3.Color = colorshex(i);
    end   
end
hold off
box on

title("Multi day measurement", 'interpreter',  'latex','fontsize',18);
xlabel("Frequency [Hz]", 'interpreter',  'latex','fontsize',18)
ylabel("Conductivity [S/m]", 'interpreter',  'latex','fontsize',18);

leg = legend('8','','', '9','','', '11','interpreter',  'latex','fontsize',14,'Location','northwest');
title(leg,'Solution', 'interpreter',  'latex','fontsize',14);

%-----relative permittivitiy

Imagsd1 = [dataa3000mgn500mg(:,4) dataa3000mgn750mg(:,4) dataa3000mgn1000mg(:,4) dataa3000mgn1250mg(:,4) dataa3000mgn1500mg(:,4) dataa3000mgn1750mg(:,4)];
Imagsd2 = [dataa3000mgn500mgd2(:,4) dataa3000mgn750mgd2(:,4) dataa3000mgn1000mgd2(:,4) dataa3000mgn1250mgd2(:,4) dataa3000mgn1500mgd2(:,4) dataa3000mgn1750mgd2(:,4)];
Imagsd3 = [dataa3000mgn500mgd3w0(:,4) dataa3000mgn750mgd3w0(:,4) dataa3000mgn1000mgd3w0(:,4) dataa3000mgn1250mgd3w0(:,4) dataa3000mgn1500mgd3w0(:,4) dataa3000mgn1750mgd3w0(:,4)];

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
    if k==2 || k==3 || k==5
       f1 = semilogy(F, permittivity1(:,k), '-', 'LineWidth', 1.5);
       f2 = semilogy(F, permittivity2(:,k), '--', 'LineWidth', 1.5);
       f3 = semilogy(F, permittivity3(:,k), ':', 'LineWidth', 1.5);
       f1.Color = colorshex(k);
       f2.Color = colorshex(k);
       f3.Color = colorshex(k);
    end       
end
hold off
box on

leg = legend('8','','', '9','','', '11', 'interpreter',  'latex','fontsize',14);
title(leg, 'Solution', 'interpreter',  'latex','fontsize',14);

title("Multi day measurement", 'interpreter',  'latex','fontsize',18);
xlabel("Frequency [Hz]", 'interpreter',  'latex','fontsize',18);
ylabel("Permittivity [F/m]", 'interpreter',  'latex','fontsize',18);
