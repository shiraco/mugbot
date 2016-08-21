import websocket
import time
import _thread as thread
import jtalk
from mugbot_expression import get_mugbot_expression


def on_message(ws, message):
    print("### recieved message ###")
    print("rsv: {}".format(message))

    exp = get_mugbot_expression
    exp.flash_eyes()
    jtalk.jtalk(message)
    exp.lighten_eyes()

def on_error(ws, error):
    print("### error ###")
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("### open ###")
    def run(*args):
        ws.send("こんにちは")
        time.sleep(1)

        # ws.close()
        # print("thread terminating...")

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    host = "192.168.11.5"
    ws = websocket.WebSocketApp("ws://" + host + ":8080/ws",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
