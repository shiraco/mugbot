import websocket
import time
import _thread as thread
from mugbot import get_mugbot


def on_message(ws, message):
    print("rsv: {}".format(message))

    mugbot = get_mugbot
    mugbot.hear(message)


def on_error(ws, error):
    print("### error ###")
    print(error)


def on_close(ws):
    print("### closed ###")
    retry_connect(ws)


def on_open(ws):
    print("### open ###")

    def run(*args):
        time.sleep(1)

    thread.start_new_thread(run, ())


def retry_connect(ws):
    ws_start()
    print("### retry_connect ###")


def ws_start():
    # host = "192.168.11.5:8080"
    host = "mugbot.herokuapp.com"
    scheme = "wss"
    url = scheme + "://" + host + "/ws"

    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
    return ws


if __name__ == "__main__":
    ws_start()
