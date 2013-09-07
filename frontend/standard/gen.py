import pystache

def img_tag(src,width="",height=""):
	return '<img src='+src+' height="'+height+' width="'+width+'" class="img-responsive" />'

def loren_ipsum():
	return "Loren Ipsum"

def btn_tag(link="#",title="Learn More"):
	return '<a class="btn btn-primary btn-lg" href="'+link+'">'+title+'</a>'

def generate():
	txt = open('frontend.mustache', 'r').read()
	'''really messy - it is a placeholder '''
	context = {'title': 'Markup', 
				'navbar': [{ "title": "Test" , "pages": [{'link': 'http://google.com','name':'Page 1'},{'link': 'http://google.com','name':'Page 2'}], 'rightnavbar': [{'link': '#','name': 'Login'}]}], 
				'rows': [{'columns': [{'width': '12', 'content': '<div class="jumbotron"><h1>Jumbotron</h1> <p>This is a simple hero unit, a simple jumbotron-style component for calling extra attention to featured content or information.</p><p><a class="btn btn-primary btn-lg">Learn more</a></p></div>'}]}
					,{'columns': [{'width': '4', 'content':'<h2>Example body text</h2><p>Nullam quis risus eget <a href="#">urna mollis ornare</a> vel eu leo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam id dolor id nibh ultricies vehicula.</p><p><small>This line of text is meant to be treated as fine print.</small></p><p>The following snippet of text is <strong>rendered as bold text</strong>.</p><p>The following snippet of text is <em>rendered as italicized text</em>.</p><p>An abbreviation of the word attribute is <abbr title="attribute">attr</abbr>.</p>'},{'width': '4', 'content': '<h2>Example body text</h2><p>Nullam quis risus eget <a href="#">urna mollis ornare</a> vel eu leo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam id dolor id nibh ultricies vehicula.</p><p><small>This line of text is meant to be treated as fine print.</small></p><p>The following snippet of text is <strong>rendered as bold text</strong>.</p><p>The following snippet of text is <em>rendered as italicized text</em>.</p><p>An abbreviation of the word attribute is <abbr title="attribute">attr</abbr>.</p>'},{'width': '4', 'content': '<h2>Example body text</h2><p>Nullam quis risus eget <a href="#">urna mollis ornare</a> vel eu leo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam id dolor id nibh ultricies vehicula.</p><p><small>This line of text is meant to be treated as fine print.</small></p><p>The following snippet of text is <strong>rendered as bold text</strong>.</p><p>The following snippet of text is <em>rendered as italicized text</em>.</p><p>An abbreviation of the word attribute is <abbr title="attribute">attr</abbr>.</p>'}]}]
			   }
	return pystache.render(txt, context)

print(generate())