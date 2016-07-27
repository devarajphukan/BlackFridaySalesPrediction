from datetime import datetime
def num_days(mnth,date,year):
	
	curr_date = mnth+'/'+date+'/'+year
	start_date = datetime.strptime('1/1/'+year, "%m/%d/%Y")
	end_date = datetime.strptime(curr_date, "%m/%d/%Y")
	return abs((end_date-start_date).days)

f = open('train_red.csv')
f1 = open('train_with_date.csv','w')
for i in f :
	try :
		j = i.strip().split(",")
		k = j[0].split(" ")
		l = k[0].split('-')
		days = str(num_days(l[1],l[2],l[0]))
		time_hr = int(k[1].split(':')[0])

		if int(k[1].split(':')[1]) > 30 :
			time_hr += 1
		time_hr = str(time_hr)

		f1.write(days+','+time_hr+','+','.join(j[1:])+'\n')
	except :
		pass
