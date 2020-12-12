from hashlib import sha256

file_hash = sha256()

n= int(input())

for i in range(1, n+1):
    BLOCK_SIZE = 65536
    address= "file%s.txt" %(str(i))
    with open(address, 'rb') as file:
        fb = file.read(BLOCK_SIZE)  # Read from the file. Take in the amount declared above
        while len(fb) > 0:  # While there is still data being read from the file
            file_hash.update(fb)  # Update the hash
            fb = file.read(BLOCK_SIZE)

pubkey= file_hash.digest()