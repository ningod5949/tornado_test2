import uuid
import datetime
import logging
from pycket.session import SessionMixin
import tornado.websocket
import tornado.web
import tornado.escape
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop

from .main import BaseHandler

logger = logging.getLogger('tudo.log')


def make_data(handler, msg, username):
    """生成我们用来发送消息的字典"""

    chat = {
        'id': str(uuid.uuid4()),
        'body': msg,
        'username': username,
        'created': str(datetime.datetime.now()),
    }
    chat['html'] = tornado.escape.to_basestring(handler.render_string('message.html', chat=chat))
    return chat

class RoomHandler(BaseHandler):
    """
    聊天室页面
    """
    @tornado.web.authenticated
    def get(self):
        # m = {
        #     'id': 1213,
        #     'username': self.current_user,
        #     'body': 'fdsfa',
        # }
        # msgs = [
        #     {
        #         'html': self.render_string('message.html', chat=m)
        #     }
        # ]
        self.render('room.html', messages=ChatHandler.history)



class ChatHandler(tornado.websocket.WebSocketHandler, SessionMixin):
    """
    处理和响应 Websocket 连接
    """
    waiters = set()   # 等待接收信息的用户
    history = []        # 存放历史消息
    history_size = 10 # 最后二十条数据

    def get_current_user(self):
        return self.session.get('tudo_user', None)

    # def open(self, *args: str, **kwargs: str):
    def open(self, *args, **kwargs):
        """
        新的 Websocket 连接打开， 自动调用
        :param args:
        :param kwargs:
        :return:
        """
        print('new ws connection: {}'.format(self))
        ChatHandler.waiters.add(self)

    def on_close(self):
        """
        Websocket 连接断开，自动调用
        :return:
        """
        print('close ws connection: {}'.format(self))
        ChatHandler.waiters.remove(self)

    def on_message(self, message):
        """
        Websocket 服务端接收到消息自动调用
        :param message:
        :return:
        """
        print("got message: {}".format(message))
        parsed = tornado.escape.json_decode(message)
        msg = parsed['body']

        if msg and msg.startswith('http://'):
            client = AsyncHTTPClient()
            save_api_url = 'http://127.0.0.1:8000/async?save_url={}'.format(msg)
            logger.info(save_api_url)

            IOLoop.current().spawn_callback(client.fetch,
                                            save_api_url,
                                            request_timeout=30)
            reply_msg = 'user {}, url {} is processing'.format(
                self.current_user,
                msg,
            )
            chat = make_data(self, reply_msg, 'system')
            self.write_message(chat)
        else:
            chat = make_data(self, msg, self.current_user)
            self.update_history(chat)
            self.send_updates(chat)

    def update_history(self, chat):
        """把新的消息更新到history， 截取最后20条"""
        ChatHandler.history.append(chat['html'])
        if len(ChatHandler.history) > ChatHandler.history_size:
            ChatHandler.history = ChatHandler.history[-ChatHandler.history_size:]

    def send_updates(self, chat):
        """给每个等待接收的用户发新消息"""
        for w in ChatHandler.waiters:
            w.write_message(chat)


class EchWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print('WebSocket 开启')

    def on_message(self, message):
        self.write_message(u'你说：' + message)

    def on_close(self):
        print('WebSocket 结束')

