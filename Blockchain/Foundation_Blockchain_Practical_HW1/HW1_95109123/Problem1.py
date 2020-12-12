import hashlib

object= 95109123
my_hash= hashlib.sha256(b'95109123').hexdigest()[-6:]

for x in reversed(range(int(1e7), int(1e8))):
    hash_object= str(x).encode()
    if hashlib.sha256(hash_object).hexdigest()[-6:] == my_hash:
        if x!= object:
            print(x)


