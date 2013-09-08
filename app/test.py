import markup

# data = markup.analyze('two_triangles.jpg')
# rows = markup.get_rows(*data)
# data3 = filter(lambda x: x != [], rows)
# print('-----------')
# for row in data3:
# 	print ("-")
# 	for item in row: 
# 		if item.box_type == 1:
# 			print "img box of width "+str(item.w)
# 		elif item.box_type != 2:
# 			print "text box of width "+str(item.w)


def process(img):
	data = markup.analyze(img)
	rows = markup.get_rows2(*data)

	data3 = filter(lambda x: x != [], rows)
	print data3
	page_structure = [];
	for row in data3:
		'''loop through the filtered data & create a sub-list for each row'''
		page_structure.append([])
		for item in row:
			'''get all indiv elems/rects from a row'''
			if item.color == 1:
				page_structure[-1].append(['img',item.w,item.color])
			elif item.color != 2:
				page_structure[-1].append(['txt',item.w,item.color])
	return filter(lambda x: x != [], page_structure) 

print(process('20130908-103116.jpg'))