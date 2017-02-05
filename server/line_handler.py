# coding: utf-8

import json
import os
from logging import DEBUG, StreamHandler, getLogger
import tornado

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# logger
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET', '')
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN', '')
LINE_DEFAULT_TO_USER = os.environ.get('LINE_DEFAULT_TO_USER', '')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
line_handler = WebhookHandler(LINE_CHANNEL_SECRET)


class Line(object):

    def __init__(self):
        self.line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
        return self


class LinePushNotifyHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
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
    @tornado.web.asynchronous
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


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    logger.debug('event: {}'.format(event))

    user_utt = event.message.text
    sys_utt = user_utt

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=sys_utt))
