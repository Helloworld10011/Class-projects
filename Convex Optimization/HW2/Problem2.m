m= mother+ mtumor;
f= [zeros(n,1); ones(mother, 1)];

A= [[-Atumor, zeros(mtumor, mother)]; [Aother, -eye(mother)]; [zeros(mother, n), -eye(mother)]];

lb= [zeros(n, 1); -inf(mother, 1)];
ub= [Bmax*ones(n, 1); inf(mother, 1)];

b= [-Dtarget*ones(mtumor, 1); Dother*ones(mother, 1); zeros(mother, 1)];

x = linprog(f, A, b, [], [], lb, ub)
%%
b= x(1:n);
tvoxel= Atumor*b;
ovoxel= Aother*b;
%%
hist(tvoxel);
title("histogram for dose of target voxels")
figure;
hist(ovoxel);
title("histogram for dose of other voxels")
%%
%comment: As we expected, most of doses for other voxels are under 0.25 and
%the mean of them is something aroud 0.2 . Also for tumor voxels, a great 
%part of them are just a little above 1.0 which would help us to minimize  
%the loss function!