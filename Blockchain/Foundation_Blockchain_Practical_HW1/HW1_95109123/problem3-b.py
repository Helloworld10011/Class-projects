import hashlib

in_dict={}
for i in range(20):
    in_dict["%s" %(str(i+1))]= input()

m= int(input())

dict = {}

for i in range(10):
    dict["h2_%s" % (str(i + 1))] = hashlib.sha256(
        (in_dict["%s" % (str(2 * i + 1))] + in_dict["%s" % (str(2 * i + 2))]).encode()).hexdigest()

for i in range(5):
    dict["h3_%s" % (str(i + 1))] = hashlib.sha256(
        (dict["h2_%s" % (str(2 * i + 1))] + dict["h2_%s" % (str(2 * i + 2))]).encode()).hexdigest()

for i in range(2):
    dict["h4_%s" % (str(i + 1))] = hashlib.sha256(
        (dict["h3_%s" % (str(2 * i + 1))] + dict["h3_%s" % (str(2 * i + 2))]).encode()).hexdigest()
dict["h4_3"] = hashlib.sha256((dict["h3_5"] + dict["h3_5"]).encode()).hexdigest()

dict['hash1'] = hashlib.sha256((dict["h4_1"] + dict["h4_2"]).encode()).hexdigest()
dict['hash2'] = hashlib.sha256((dict["h4_3"] + dict["h4_3"]).encode()).hexdigest()

print(hashlib.sha256((dict["hash1"] + dict["hash2"]).encode()).hexdigest())

i=m
print(in_dict["%s" %(str((i-1)*(i%2 == 0) + (i+1)*(i%2 != 0)))])
i= (i+1)//2
print(dict["h2_%s" %(str((i-1)*(i%2 ==0)+ (i+1)*(i%2 != 0)))])
i= (i+1)//2
if i<=4:
    print(dict["h3_%s" %(str((i-1)*(i%2 ==0)+ (i+1)*(i%2 != 0)))])
else:
    print(dict["h3_5"])
i=(i+1)//2
if i<=2:
    print(dict["h4_%s" %(str((i-1)*(i%2 ==0)+ (i+1)*(i%2 != 0)))])
else:
    print(dict["h4_3"])
i=(i+1)//2
print(dict["hash%s" %(str((i-1)*(i%2 ==0)+ (i+1)*(i%2 != 0)))])