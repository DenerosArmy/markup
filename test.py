import markup

data = markup.analyze('00000001.jpg')
rows = markup.get_rows(*data)
data3 = filter(lambda x: x != [], rows)
print('-----------')
for row in data3:
	for item in row: 
		print item.w
