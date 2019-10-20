import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options

from handlers import main, account

define('port', default='8000', help='Listening port', type=int)
define('debug', default='True', help='Debug mode', type=bool)


class Application(tornado.web.Application):
    def __init__(self, debug=False):
        handlers = [
            (r'/', main.IndexHandler),
            (r'/explore', main.ExploreHandler),
            (r'/post/(?P<post_id>[0-9]+)', main.PostHandler),
            (r'/signup', account.RegisterHandler),
        ]

        settings = dict(
            debug=True,
            template_path='templates',
            static_path='static',
        )
        super().__init__(handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    application = Application(debug=options.debug)
    application.listen(options.port)
    print('server start on port {}'.format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()


