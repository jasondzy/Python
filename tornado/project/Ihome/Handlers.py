import tornado.web

class BaseHandler(tornado.web.RequestHandler):
	pass

class IndexHandler(BaseHandler):
	def get(self):
		self.write('ok')