import hashlib
my_hash1= hashlib.sha256(b'95109123').hexdigest()
my_hash2= hashlib.sha256(b'95109134').hexdigest()
print(my_hash1, my_hash2)
print((my_hash1+my_hash2).encode())