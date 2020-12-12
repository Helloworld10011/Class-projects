A=imread('HajiFirouz.jpg'); 
A=im2double(A); 
A=rgb2gray(A);

n_list= floor(linspace(1, 395, 50));
errors= zeros(length(n_list), 1);

[U, S, V]= svd(A);

for k= 1:length(n_list)
    n= n_list(k);
    Ap= U(:, 1:n)*(S(1:n, 1:n))*V(:, 1:n)';
    errors(k)= sqrt(sum(sum((A-Ap).^2)));
end

scatter(n_list, errors, '.')

%%
n= 100;
A_compressed= U(:, 1:n)*(S(1:n, 1:n))*V(:, 1:n)';
imshow(A_compressed)