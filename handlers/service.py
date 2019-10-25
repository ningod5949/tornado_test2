import time
import logging
import requests
from tornado.httpclient import AsyncHTTPClient
from tornado.gen import coroutine, sleep
from handlers.main import BaseHandler
from utils.photo import UploadImage
from .chat import ChatHandler, make_data


url = 'http://pic1.win4000.com/wallpaper/2018-05-08/5af150aea45bd.jpg'
urlq = 'http://source.unsplash.com/random'

logger = logging.getLogger('tudo.log')

class SyncSaveHandler(BaseHandler):
    def get(self):
        save_url = self.get_argument('save_url', '')
        logger.info(save_url)
        # print(save_url)

        resp = requests.get(save_url)
        time.sleep(5)

        logger.info(str(resp.status_code) + '++++++++++++++++++++')
        # up_img = UploadImage('x.jpg', self.settings['static_path'])
        # up_img.save_upload(resp.content)
        # up_img.make_thumb()
        #
        # post_id = self.orm.add_post(up_img.image_url,
        #                   up_img.thumb_url,
        #                   self.current_user)

        # self.redirect('/post/{}'.format(post_id))


class AsyncSaveHandler(BaseHandler):
    @coroutine
    def get(self):
        username = self.get_argument('name', '')
        save_url = self.get_argument('save_url', '')
        is_from_room = self.get_argument('is_from', '') == 'room'
        logger.info(save_url)
        logger.info(is_from_room)
        logger.info(self.request.remote_ip)

        if not is_from_room:
            self.write('error')
            return

        client = AsyncHTTPClient()
        resp = yield client.fetch(save_url, request_timeout=30)
        logger.info(resp.code)

        # time.sleep(15)
        # yield sleep(15)
        # logger.info('sleep end')
        # self.write('get end')

        up_img = UploadImage('x.jpg', self.settings['static_path'])
        up_img.save_upload(resp.body)
        up_img.make_thumb()

        post_id = self.orm.add_post(up_img.image_url,
                                    up_img.thumb_url,
                                    username)

        # self.redirect('/post/{}'.format(post_id))
        msg = 'user {} post: http://127.0.0.1:8000/post/{}'.format(username, post_id)
        chat = make_data(self, msg, img_url=up_img.thumb_url, post_id=post_id)
        ChatHandler.update_history(chat)
        ChatHandler.send_updates(chat)
