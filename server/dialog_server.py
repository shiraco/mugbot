import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.options
import tornado.httpserver
import os
from logging import DEBUG, StreamHandler, getLogger

from line_handler import (
    LineWebhookHandler, LinePushNotifyHandler
)

# logger
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class IndexHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self, *args):
        self.render("index.html")


class SocketHandler(tornado.websocket.WebSocketHandler):

    clients = []
    ws_messages = []

    def check_origin(self, origin):
        return True

    def open(self):
        logger.debug('open')
        if self not in self.clients:
            self.clients.append(self)

    def on_message(self, message):
        logger.debug('message {}'.format(message))
        # for client in self.clients:
        #     client.write_message(message)
        SocketHandler.send_message(message)

    def on_close(self):
        logger.debug('close')
        if self in self.clients:
            self.clients.remove(self)

    @classmethod
    def send_message(cls, message):

        cls.ws_messages.append(message)

        for robot in cls.clients:
            robot.write_message(message)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/ws', SocketHandler),
            (r'/webhook', LineWebhookHandler),
            (r'/push', LinePushNotifyHandler),
        ]
        settings = dict(
            cookie_secret='__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__',
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            xsrf_cookies=False,
        )

        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    port = int(os.environ.get("PORT", 8080))
    http_server.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
