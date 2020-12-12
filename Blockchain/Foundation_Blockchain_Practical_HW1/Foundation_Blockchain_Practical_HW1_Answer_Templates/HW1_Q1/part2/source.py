import hashlib
import numpy as np

class CollisionFinder:
    def __init__(self):
        pass

    def findCollision(self): #Do not change the name of the function
        N=16000
        n= int(N/2)
        x = np.random.choice(np.arange(2**14, dtype= int), (N, ), replace=False)
        u, p= (x[:n], x[n:])

        uset= []
        pset= []

        ob_hash1 = str(u[0]).encode()
        ob_hash2 = str(p[0]).encode()

        uset.append(hashlib.sha256(ob_hash1).hexdigest()[-6:])
        pset.append(hashlib.sha256(ob_hash2).hexdigest()[-6:])

        for i in range(1, n):
            ob_hash1 = str(u[i]).encode()
            ob_hash2 = str(p[i]).encode()

            hash1= hashlib.sha256(ob_hash1).hexdigest()[-6:]
            hash2= hashlib.sha256(ob_hash2).hexdigest()[-6:]


            if hash1 in uset and hash2 in pset:
                index1= uset.index(hash1)
                index2= pset.index(hash2)
                return [str(u[index1]), str(u[i]), str(p[index2]), str(p[i])]

            if hash1 in uset:
                index1 = uset.index(hash1)
                for k in range(i, n):
                    ob_hash2 = str(p[k]).encode()
                    hash2 = hashlib.sha256(ob_hash2).hexdigest()[-6:]
                    if hash2 in pset:
                        index2 = pset.index(hash2)
                        return [str(u[index1]), str(u[i]), str(p[index2]), str(p[k])]
                    pset.append(hash2)

            if hash2 in pset:
                index2 = pset.index(hash2)
                for k in range(i, n):
                    ob_hash1 = str(u[k]).encode()
                    hash1 = hashlib.sha256(ob_hash1).hexdigest()[-6:]
                    if hash1 in uset:
                        index1 = uset.index(hash1)
                        return [str(u[index1]), str(u[k]), str(p[index2]), str(p[i])]
                    uset.append(hash1)

            uset.append(hash1)
            pset.append(hash2)
