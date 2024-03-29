import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options

from handlers import main, account, chat, service

define('port', default='8000', help='Listening port', type=int)
define('debug', default='True', help='Debug mode', type=bool)


class Application(tornado.web.Application):
    def __init__(self, debug=False):
        handlers = [
            (r'/', main.IndexHandler),
            (r'/explore', main.ExploreHandler),
            (r'/post/(?P<post_id>[0-9]+)', main.PostHandler),
            (r'/upload', main.UploadHandler),
            (r'/profile', main.ProfileHandler),
            (r'/like', main.LikeH),
            (r'/signup', account.RegisterHandler),
            (r'/login', account.LoginHandler),
            (r'/logout', account.LogoutHandler),
            (r'/ws/echo', chat.EchWebSocket),           # 聊天
            (r'/ws', chat.ChatHandler),           # 聊天
            (r'/room', chat.RoomHandler),           # 聊天
            (r'/sync', service.SyncSaveHandler),
            (r'/async', service.AsyncSaveHandler),
        ]

        settings = dict(
            debug=True,
            template_path='templates',
            static_path='static',
            cookie_secret='fkjdshfkjsadfhdkjsaf',
            login_url='/login',
            # xsrf_cookies=True
            pycket={
                'engine': 'redis',
                'storage': {
                    'host': 'localhost',
                    'port': '6379',
                    'db_sessions': 5,
                    'max_connections': 2 ** 30,
                },
                'cookies': {
                    'expires_days': 30,
                },
            }
        )
        super().__init__(handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    application = Application(debug=options.debug)
    application.listen(options.port)
    print('server start on port {}'.format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()


