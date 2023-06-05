import csv


data = []
with open('dataset.csv', 'r') as file:

    reader = csv.reader(file)

    for row in reader:
        data.append(row)

data.pop(0)
for i in range(len(data)):
	if data[i][1]=='Positive':
		data[i][1]='1'
	else:
		data[i][1]='0'

with open("data.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    for row in data:
        writer.writerow(row)