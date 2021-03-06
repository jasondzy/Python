import tornado.web
import tornado.options
import tornado.httpserver
import tornado.ioloop
import os
import models
import Handlers
import base64, uuid
from tornado.web import url, StaticFileHandler

tornado.options.define('port', default=8000, type=int, help=' runserver on given port')


class Application(tornado.web.Application):
	def __init__(self):
		################# create mysql object #######
		self.mysql = models.HandleMysql()
		self.mysql.create_table()
		################# end #######################
		################# create redis object #######
		self.redis = models.HandRedis()
		################# end #######################

		################# 进行域名地址的映射 ##########
		super(Application, self).__init__(
		[
		# url(r'^/$', Handlers.IndexHandler, name="IndexHandler"), #这里不采用get中的render返回index的原因是因为，index.html中使用了index.js脚本中的$.get等方式来和后台通讯从而获得数据，而render方式处理模板的时候会对模板进行解析处理会报错，只能通过直接加载index.html的方式
		url(r'/api/house/index', Handlers.House_index, dict(database = self.mysql, database_redis = self.redis), name="House_index"),
		url(r'^/register$', Handlers.House_register, dict(database = self.mysql, database_redis = self.redis), name="House_register"),
		url(r'^/api/piccode$', Handlers.PicCodeHandler, dict(database = self.mysql, database_redis = self.redis), name="PicCodeHandler"),
		url(r'^/api/smscode$', Handlers.Smscode, dict(database = self.mysql, database_redis = self.redis), name="Smscode"),
		url(r'^/api/register$', Handlers.Register_verity, dict(database = self.mysql, database_redis = self.redis), name="Register_verity"),
		url(r'^/api/login$', Handlers.Login_verity, dict(database = self.mysql, database_redis = self.redis), name="database = self.mysql"),
		url(r'^/api/check_login$', Handlers.Check_login, dict(database = self.mysql, database_redis = self.redis), name="Check_login"),
		url(r'^/api/profile$', Handlers.Personal_info, dict(database = self.mysql, database_redis = self.redis), name="Personal_info"),
		url(r'^/api/profile/name$', Handlers.Personal_name, dict(database = self.mysql, database_redis = self.redis), name="Personal_name"),
		url(r'^/api/profile/avatar$', Handlers.Personal_img, dict(database = self.mysql, database_redis = self.redis), name="Personal_img"),
		url(r'^/api/house/info$', Handlers.House_info, dict(database = self.mysql, database_redis = self.redis), name="House_info"),
		url(r'^/api/order$', Handlers.House_reserve, dict(database = self.mysql, database_redis = self.redis), name="House_reserve"),
		url(r'^/api/order/my$', Handlers.Show_order, dict(database = self.mysql, database_redis = self.redis), name="Show_order"),
		url(r'^/api/profile/auth$', Handlers.Real_name_verity, dict(database = self.mysql, database_redis = self.redis), name="Real_name_verity"),
		url(r'^/api/house/my$', Handlers.Myhouse_show, dict(database = self.mysql, database_redis = self.redis), name="Myhouse_show"),
		url(r'^/api/house/list2$', Handlers.House_list_handler, dict(database = self.mysql, database_redis = self.redis), name = "House_list_handler"),
		url(r'^/api/house/area$', Handlers.Area_info_handler, dict(database = self.mysql, database_redis = self.redis), name="Area_info_handler"),
		url(r'^/api/logout$', Handlers.Login_out, dict(database = self.mysql, database_redis = self.redis), name = "Login_out"),
		url(r'/(.*)',StaticFileHandler, {"path":os.path.join(os.path.dirname(__file__),"template"), "default_filename":"index.html"}, name="index"),
		],
		################# end ########################
		debug = True, 
		static_path = os.path.join(os.path.dirname(__file__), 'static'),
		template_path = os.path.join(os.path.dirname(__file__), 'template'),
		cookie_secret = str(base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)), #这里使用uuid和base64共同合成了一个随机的字符串，添加到cookie从而形成secure_cookie的机制
		xsrf_cookies = True,
		)


def main():
	tornado.options.parse_command_line()

	app = Application()

	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(8000) 

	tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
	main()