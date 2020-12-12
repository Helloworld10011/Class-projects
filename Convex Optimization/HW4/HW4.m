clear all
clc

m= 4;
n= 10;
while true
  q = randn(n, n);
  if rank(q) == n; break; end    %will be true nearly all the time
end
Q= q' * q;

c= randn(n, 1);
A= randn(m ,n);
b= randn(m, 1);
%%
[x, y, s, ~, value, k]= prim_dual_optim(Q, c, A, b, 0.5, 1e-5, 1e-5, 1e-5, 0.99)
%%
cvx_begin
    variable x(10) nonnegative
    minimize(0.5*x'*Q*x+c'*x)
    subject to
        A*x-b == 0;
cvx_end
%%
[~, ~, ~, resids, ~, ~]= prim_dual_optim(Q, c, A, b, 0.5, 1e-5, 1e-5, 1e-5, 0.99);
plot(resids);
title("value of ||XSe- miu*e|| by iteration")
%%
function [x, y, s, resids, value, k]= prim_dual_optim(Q, c, A, b, sigma, epsilon_0, epsilon_d, epsilon_p, alpha_0)
    [m, n]= size(A);
    p_check= @(e)(norm(e)/(1+norm(b)) <= epsilon_p);
    d_check= @(e)(norm(e)/(1+norm(c)) <= epsilon_d);
    zero_check= @(e, f)( e'*f/(n*(1+abs(c'*e+0.5*e'*Q*e))) <= epsilon_0);
    
    k=0;
    x= rand(n, 1);
    y= zeros(m, 1);
    s= rand(n, 1);
    miu= x'*s/n;
    xsi_p= b- A*x;
    xsi_d= c- A'*y- s+Q*x;
    
    resids= [];
    
    while ~p_check(xsi_p) || ~d_check(xsi_d) || ~zero_check(x, s)
        M= [A, zeros(m, m), zeros(m, n); -Q, A', eye(n); diag(s), zeros(n, m), diag(x)];
        r= [xsi_p; xsi_d; miu*ones(n, 1)- diag(x)*diag(s)*ones(n, 1)];
        
        delta= linsolve(M, r);
        delta_x= delta(1:n);
        delta_y= delta(n+1:n+m);
        delta_s= delta(n+m+1:2*n+m);
        
        u= x./delta_x;
        alpha_p= abs(max(u(delta_x<0)));
        if isempty(alpha_p)==1; alpha_p=1; end
        u= s./delta_s;
        alpha_d= abs(max(u(delta_s<0)));
        if isempty(alpha_d)==1; alpha_d=1; end
        
        x= x+ alpha_0*alpha_p*delta_x;
        y= y+ alpha_0*alpha_d*delta_y;
        s= s+ alpha_0*alpha_d*delta_s;
        
        xsi_p= b- A*x;
        xsi_d= c- A'*y- s+Q*x;
        k= k+1;
        
        resids= [resids, norm((diag(x)*diag(s)*ones(n, 1)- miu*ones(n, 1)), 2)];
        
        miu= miu*sigma;
    end
    
    value= 0.5*x'*Q*x + c'*x;
    
end