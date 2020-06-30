import tornado.web


class HandlerIndexPage(tornado.web.RequestHandler):
    def initialize(self, helper):
        self.helper = helper

    def get(self):
        ip = self.helper.interfaces_first()
        self.render("index.html", ip=ip)
