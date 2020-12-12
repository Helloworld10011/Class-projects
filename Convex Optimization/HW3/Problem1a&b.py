from cvxpy import *
import numpy as np
import time

for (m, n) in [(1, 2), (3, 5), (5, 10), (10, 20), (20, 50)]:
    print("Checking for (n, m)= (%i, %i)..." %(n, m))
    c= Parameter(n)
    b= Parameter(m)
    A= Parameter((m, n))

    x= Variable(n)
    func1= c*x
    obj1= Minimize(func1)
    cnstr1= [A@x == b, x>=0, x<= 1]
    prob1= Problem(obj1, cnstr1)

    v= Variable(m)
    func2= -b*v + sum(minimum(0, A.T @ v + c))
    obj2= Maximize(func2)
    prob2= Problem(obj2)

    for _ in range(5):
        c.value= np.random.randn(n)
        mat= np.random.randn(m, n)
        A.value = mat
        b.value = mat @ (np.random.rand(n))
        tic= time.time()
        prob1.solve()
        toc= time.time()
        print("LP Relaxation solved in %fs and min= %f" %(toc -tic, func1.value))

        tic = time.time()
        prob2.solve()
        toc = time.time()
        print("Lagrange Relaxation solved in %fs and max= %f" % (toc - tic, func2.value))




"""
comment:
I saw nothing prominent in change of computational time by varying dimensions(n, m)!
"""