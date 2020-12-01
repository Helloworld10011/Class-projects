import csv
with open('H110desc.csv', encoding="utf8") as file:
    csv_reader = csv.reader(file)
    votes = []
    for row in csv_reader:
        print(row)



