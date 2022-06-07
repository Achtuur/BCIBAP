a = rand(1, 10);
b = rand(1, 10) * 10;
t = 1:10;

hold on;
yyaxis left;
plot(t, a);
yyaxis right;
plot(t,b);
hold on;