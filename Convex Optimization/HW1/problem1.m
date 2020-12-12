n= 1e5;
m=1000;
y1= 50* rand(n, 1) -25;
y2= 50* rand(n, 1) -25;

count=0;
y1_true= zeros(n, 1);
y2_true= zeros(n, 1);

for k= 1:n
    x1= 20* rand(m, 1)- 20;
    x2= 20* rand(m, 1)- 20;
    if all((2*(x1.^4)+(x2.^4)+y1(k)*x1.*(x2.^3)+y2(k)*(x1.^3).*x2) >= 0)
        count =count+ 1;
        y1_true(count)= y1(k);
        y2_true(count)= y2(k);
    end
end

scatter(y1_true(1:count), y2_true(1:count), '.')
