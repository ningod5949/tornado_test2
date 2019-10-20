import os
from uuid import uuid4

from PIL import Image


class UploadImage(object):
    """
    辅助保存用户上传的图片，生成对应得缩略图，记录图片相关的URL用来保存到数据库
    """
    upload_dir = 'uploads'
    thumb_dir = 'thumbs'
    thumb_size = (200, 200)
    def __init__(self, name, static_path):
        self.new_name = self.gen_new_name(name)
        self.static_path = static_path

    def gen_new_name(self, name):
        """
        生成唯一的字符串，用作图片名字
        :return:
        """
        _, ext = os.path.splitext(name)
        return uuid4().hex + ext

    @property
    def image_url(self):
        return os.path.join(self.upload_dir, self.new_name)

    @property
    def save_path(self):
        return os.path.join(self.static_path, self.image_url)

    def save_upload(self, content):
        with open(self.save_path, 'wb') as fh:
            fh.write(content)

    @property
    def thumb_url(self):
        name, ext = os.path.splitext(self.new_name)
        thumb_name = '{}_{}x{}{}'.format(name,
                                         self.thumb_size[0],
                                         self.thumb_size[1],
                                         ext)
        return os.path.join(self.upload_dir, self.thumb_dir, thumb_name)

    def make_thumb(self):
        """
        生成缩略图
        :param path:
        :return:
        """
        im = Image.open(self.save_path)
        im.thumbnail(self.thumb_size)
        save_path = os.path.join(self.static_path, self.thumb_url)
        im.save(save_path, 'JPEG')