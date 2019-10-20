import tornado.web
from PIL import Image
from pycket.session import SessionMixin

from utils.account import add_post, get_all_posts, get_post, get_posts_for
from utils.photo import UploadImage


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('tudo_user', None)


class IndexHandler(BaseHandler):
    """
    首页，用户上传图片的展示
    """
    @tornado.web.authenticated
    def get(self):
        posts = get_posts_for(self.current_user)
        self.render('index.html', posts=posts)


class ExploreHandler(BaseHandler):
    """
    最近上传缩略图的页面
    """
    @tornado.web.authenticated
    def get(self):
        posts = get_all_posts()
        self.render('explore.html', posts=posts)


class PostHandler(BaseHandler):
    """
    单个图片详情页面
    """
    def get(self, post_id):
        post = get_post(post_id)
        user = post.user
        if not post:
            self.write('wrong id {}'.format(post_id))
        else:
            self.render('post.html', post=post, user=user)


class UploadHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('upload.html')

    @tornado.web.authenticated
    def post(self):
        pics = self.request.files.get('picture', [])        # 拿到上传的图片
        post_id = 1
        for p in  pics:
            up_img = UploadImage(p['filename'], self.settings['static_path'])
            up_img.save_upload(p['body'])
            up_img.make_thumb()
            post_id = add_post(up_img.image_url,
                               up_img.thumb_url,
                               self.current_user)

        self.redirect('/post/{}'.format(post_id))