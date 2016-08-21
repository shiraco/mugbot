import tornado.ioloop
import tornado.web
import tornado.websocket
import subprocess


class Messenger(tornado.websocket.WebSocketHandler):

    clients = []

    def check_origin(self, origin):
        return True

    def open(self):
        print('open')
        if self not in self.clients:
            self.clients.append(self)

    def on_message(self, message):
        print('message {}'.format(message))
        for client in self.clients:
            client.write_message("さようなら")

    def on_close(self):
        print('close')
        if self in self.clients:
            self.clients.remove(self)

application = tornado.web.Application([(r'/ws', Messenger)])

if __name__ =="__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.current().start()
