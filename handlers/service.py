import requests

from handlers.main import BaseHandler
from utils.photo import UploadImage

url = 'http://pic1.win4000.com/wallpaper/2018-05-08/5af150aea45bd.jpg'

class SyncSaveHandler(BaseHandler):
    def get(self):
        save_url = self.get_argument('save_url', '')
        print(save_url)

        resp = requests.get(save_url)
        up_img = UploadImage('x.jpg', self.settings['static_path'])
        up_img.save_upload(resp.content)

        post_id = self.orm.add_post(up_img.image_url,
                          up_img.thumb_url,
                          self.current_user)

        self.redirect('/post/{}'.format(post_id))