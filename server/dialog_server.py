import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.options
import tornado.httpserver
import os
import json

from logging import DEBUG, StreamHandler, getLogger

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET', '')
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN', '')
LINE_DEFAULT_TO_USER = os.environ.get('LINE_DEFAULT_TO_USER', '')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
line_handler = WebhookHandler(LINE_CHANNEL_SECRET)


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
    messages = []

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

        cls.messages.append(message)

        for client in cls.clients:
            client.write_message(message)


class LinePushNotifyHandler(tornado.web.RequestHandler):

    def get(self, *args):

        to = self.get_argument('to', default=LINE_DEFAULT_TO_USER)
        text = self.get_argument('text', default='Hello World!')

        logger.debug('to user: {}'.format(to))

        try:
            line_bot_api.push_message(to, TextSendMessage(text=text))

        except LineBotApiError:
            raise tornado.web.HTTPError(500, 'LINE bot api error')

        self.write(json.dumps('OK'))


class LineWebhookHandler(tornado.web.RequestHandler):

    def post(self, *args):

        signature = self.request.headers.get('X-Line-Signature')
        body = self.request.body

        if not body:
            raise tornado.web.HTTPError(400, 'Empty request body',
                                        'A valid JSON document is required.')

        body = body.decode('utf-8')
        logger.debug('receive_params: {}'.format(json.loads(body)))

        # handle webhook body
        try:
            line_handler.handle(body, signature)

        except InvalidSignatureError:
            raise tornado.web.HTTPError(400, 'Invalid signature error.')

        self.write(json.dumps('OK'))


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


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    logger.debug('event: {}'.format(event))

    user_utt = event.message.text
    robot_utt = user_utt + "だってさ！"

    SocketHandler.send_message(robot_utt)
    logger.debug('say: {}'.format(robot_utt))

    sys_utt = "伝えといたよー"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=sys_utt))


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    port = int(os.environ.get("PORT", 8080))
    http_server.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
