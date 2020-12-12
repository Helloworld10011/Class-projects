n=3;
N=4*1e4;
A1= randn(n);
A2= randn(n);
Q1= 1/2*(A1+A1');
Q2= 1/2*(A2+A2');

x= randn(n, N);
x= x./((sum(x.^2)).^0.5);

y1= diag(x'*Q1*x);
y2= diag(x'*Q2*x);

scatter(y1, y2, '.')
