import tornado.web
from PIL import Image
from pycket.session import SessionMixin

from utils.account import add_post, get_all_posts, get_post


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('tudo_user', None)


class IndexHandler(tornado.web.RequestHandler):
    """
    首页，用户上传图片的展示
    """
    def get(self):
        posts = get_all_posts()
        self.render('index.html', posts=posts)


class ExploreHandler(tornado.web.RequestHandler):
    """
    最近上传缩略图的页面
    """
    def get(self):
        self.render('explore.html')


class PostHandler(tornado.web.RequestHandler):
    """
    单个图片详情页面
    """
    def get(self, post_id):
        post = get_post(post_id)
        if not post:
            self.write('wrong id {}'.format(post_id))
        else:
            self.render('post.html', post=post)


class UploadHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('upload.html')

    @tornado.web.authenticated
    def post(self):
        pics = self.request.files.get('picture', [])        # 拿到上传的图片
        post_id = 1
        for p in  pics:
            save_path = 'static/upload/{}'.format(p['filename'])

            with open(save_path, 'wb') as fh:
                fh.write(p['body'])

            post_id = add_post('upload/{}'.format(p['filename']), self.current_user)
            im = Image.open(save_path)
            im.thumbnail((200, 200))
            im.save('static/upload/thumb_{}.jpg'.format(p['filename']), 'JPEG')
        self.redirect('/post/{}'.format(post_id))