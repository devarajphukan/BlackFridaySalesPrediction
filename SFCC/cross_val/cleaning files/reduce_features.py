import csv
f1 = open('train_red.csv','w')
with open('train.csv', 'rb') as f:
	reader = csv.reader(f)
	for row in reader:
		k = row[0]+','+row[1]+','+row[3]+','+row[4]+','+row[7]+','+row[8]
		f1.write(k+'\n')
	
f2 = open('test_red.csv','w')
with open('test.csv', 'rb') as f:
	reader = csv.reader(f)
	for row in reader:
		k = row[1]+','+row[2]+','+row[3]+','+row[5]+','+row[6]
		f2.write(k+'\n')