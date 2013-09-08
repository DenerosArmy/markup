import pystache
import test

def img_tag(src,width="",height=""):
	return '<img src='+src+' height="'+str(height)+'" width="'+str(width)+'" class="img-responsive" />'

def loren_ipsum():
	return '<h2>Example body text</h2><p>Nullam quis risus eget <a href="#">urna mollis ornare</a> vel eu leo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam id dolor id nibh ultricies vehicula.</p><p><small>This line of text is meant to be treated as fine print.</small></p><p>The following snippet of text is <strong>rendered as bold text</strong>.</p><p>The following snippet of text is <em>rendered as italicized text</em>.</p><p>An abbreviation of the word attribute is <abbr title="attribute">attr</abbr>.</p>'

def jumbotron(style=""):
	return '<div class="jumbotron" style="'+style+'"><h1>Hello World!</h1> <p>This is a simple hero unit, a simple jumbotron-style component for calling extra attention to featured content or information.</p><p><a class="btn btn-primary btn-lg">Learn more</a></p></div>'
def btn_tag(link="#",title="Learn More"):
	return '<a class="btn btn-primary btn-lg" href="'+link+'">'+title+'</a>'

def generate(rows,auto_expand=True):
	txt = open('frontend.mustache', 'r').read()
	'''rows is like [[['img', 5, 1], ['img', 5, 1]], [['txt', 11, 0]]]'''
	actual_content = []
	for row in rows:
		cols =  []
		for elem in row:
			'''elem[1] is the width'''
			if elem[0] == "img":
				content = img_tag('http://placekitten.com/600/400',400,300)
			elif elem[1] >= 44:
				#if elem[0] == "img":
				content = jumbotron()
			else: 
				content = loren_ipsum()
			cols.append({'width': str(elem[1]/4), 'content':  content })
		actual_content.append({'columns' : cols})
	context = {'title': 'Markup', 'footer': 'True', 'navbar': [{ "title": "PennApps" , "pages": [{'link': 'http://google.com','name':'About'},{'link': 'http://google.com','name':'Contact'}], 'rightnavbar': [{'link': '#','name': 'Login'}]}], 
				'rows': actual_content
			   }
	return pystache.render(txt, context)

def create(pic='two_triangles.jpg',result='generated2.html'):
	rows = test.process(pic)
	page = generate(rows)
	myfile = open(result,"w")
	myfile.write(page)
	return 'http://192.241.136.149:8000/'+result



