f = open('train_with_dist.csv')
li_day = []
li_county = []
li_crime = []

for i in f :
	j = i.strip().split(',')
	
	k = str(j[3].strip())
	li_day.append(k)
	l = str(j[4].strip())
	li_county.append(l)
	m = str(j[2].strip())
	li_crime.append(m)

days = list(set(li_day))
counties = list(set(li_county))
crimes = list(set(li_crime))

crimes_cat = {}
cat_crimes = {}
for i in range(len(crimes)) :
	crimes_cat[crimes[i]] = str(i)
	cat_crimes[str(i)] = crimes[i]

fjson = open('crimes.json','w')
fjson.write(str(cat_crimes)) 

counties_cat = {}
for i in range(len(counties)) :
	counties_cat[counties[i]] = str(i+1)
# print counties_cat
days_cat = {}
for i in range(len(days)) :
	days_cat[days[i]] = str(i+1)
# print days_cat

f1 = open('train_with_dist.csv')
f2 = open('train_cat.csv','w')
f2.write('date,hour,crime,day,county,distance\n')
for i in f1 :
	j = i.strip().split(',')
	j[2] = crimes_cat[j[2]]
	j[3] = days_cat[j[3]]
	j[4] = counties_cat[j[4]]
	# print ','.join(j)
	f2.write(','.join(j)+'\n')