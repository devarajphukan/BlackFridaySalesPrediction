f = open('test_with_dist.csv')
li_day = []
li_county = []

for i in f :
	j = i.strip().split(',')
	k = str(j[2].strip())
	li_day.append(k)
	l = str(j[3].strip())
	li_county.append(l)

days = list(set(li_day))
counties = list(set(li_county))

counties_cat = {}
for i in range(len(counties)) :
	counties_cat[counties[i]] = str(i+1)
# print counties_cat
days_cat = {}
for i in range(len(days)) :
	days_cat[days[i]] = str(i+1)
# print days_cat

f1 = open('test_with_dist.csv')
f2 = open('test_cat.csv','w')
f2.write('date,hour,day,county,distance\n')
for i in f1 :
	j = i.strip().split(',')
	j[2] = days_cat[j[2]]
	j[3] = counties_cat[j[3]]
	# print ','.join(j)
	f2.write(','.join(j)+'\n')