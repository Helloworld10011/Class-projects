import hashlib

#Do not change the name of this class
class MerkleTreeCalculator:
    #use this function for hashing a file
    def __init__(self):
        pass

    def sha256sum(self, filename):
        h = hashlib.sha256()
        with open(filename, 'rb', buffering=0) as f:
            for b in iter(lambda: f.read(128 * 1024), b''):
                h.update(b)
        return h.hexdigest()

    #Do not change the name of this function
    def calculate_merkle_root(self):
        dict={}
        for i in range(20):
            dict["h1_%s" %(str(i+1))]= self.sha256sum('resource/file%s.txt' %(str(i+1)))

        for i in range(10):
            dict["h2_%s" %(str(i+1))]= hashlib.sha256((dict["h1_%s" %(str(2*i+1))]+dict["h1_%s" %(str(2*i+2))]).encode()).hexdigest()

        for i in range(5):
            dict["h3_%s" %(str(i+1))]= hashlib.sha256((dict["h2_%s" %(str(2*i+1))]+dict["h2_%s" %(str(2*i+2))]).encode()).hexdigest()

        for i in range(2):
            dict["h4_%s" % (str(i + 1))] = hashlib.sha256(
                (dict["h3_%s" % (str(2 * i + 1))] + dict["h3_%s" % (str(2 * i + 2))]).encode()).hexdigest()
        dict["h4_3"]= hashlib.sha256((dict["h3_5"] + dict["h3_5"]).encode()).hexdigest()

        hash1 = hashlib.sha256((dict["h4_1"]+dict["h4_2"]).encode()).hexdigest()
        hash2 = hashlib.sha256((dict["h4_3"] + dict["h4_3"]).encode()).hexdigest()

        return hashlib.sha256((hash1+hash2).encode()).hexdigest()


mine= MerkleTreeCalculator()
print(mine.calculate_merkle_root())