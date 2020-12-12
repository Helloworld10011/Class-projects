import math

q= int(input())
X= []
for i in range(q):
    p= int(input())
    g= int(input())
    y= int(input())
    n= int(math.log2(p-1))

    if y==1:
        X.append(p-1)
        continue
#    if y==g:
#        X.append(1)
#        continue
    x= 0
    alpha=1
    beta = int((p-1)/2)
    for j in range(n):
        pow1= pow(g, x, p)
        if pow1==y: break
        if pow(y, beta, p) != pow(pow1, beta ,p):
            x+= alpha
        alpha*= 2
        beta= int(beta/2)
    X.append(x)

[print(x) for x in X]



