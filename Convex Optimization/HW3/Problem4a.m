d= [2; 1.24; 0.59; 1.31; 1.44];
y= [1.8, 2, 1.5, 1.5, 2.5; 2.5, 1.7, 1.5, 2.0, 1.5];

A= [-2*y', ones(5, 1)];
b= d.^2- (sum(y).^2)';
D= [eye(2), zeros(2, 1); zeros(1, 2), 0];
f= [zeros(2, 1); -0.5];

cvx_begin sdp
    variable t
    variable v
    maximize(sum(b.^2)- t)
    subject to
        [A'*A + v*D, A'*b- v*f; (A'*b- v*f)', t] >= 0;
cvx_end
cvx_value
       
v