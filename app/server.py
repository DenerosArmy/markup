import tornado.ioloop
import tornado.web
import tornado.options as opt
import StringIO
import Image
import urllib
import gen
from datetime import *

opt.define("port", default = 3000, help = "Server Port Number", type = int)

class ImageHandler(tornado.web.RequestHandler):
    def get(self):	
	url = self.get_argument("url")  
	if (url):
		name = datetime.now().strftime("%Y%m%d-%H%M%S")
		urllib.urlretrieve(url, name+".jpg")
		print gen.create(name+".jpg",name+".html")
		print "RETRIEVED"
		return "http://192.241.136.149:3000/"+name+".html"
	return "hello"

application = tornado.web.Application([
    (r"/photos", ImageHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, dict(path=".")),
])

if __name__ == "__main__":
    print("Server running on port {0}".format(opt.options.port))
    application.listen(opt.options.port)
    tornado.ioloop.IOLoop.instance().start()
