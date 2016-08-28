import websocket
import time
import _thread as thread
from mugbot import get_mugbot


retry_attempts = 0
max_retry_attempts = 120


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
        # ws.send("うーん")
        time.sleep(1)

        # ws.close()
        # print("thread terminating...")

    thread.start_new_thread(run, ())

def retry_connect(ws):
    if retry_attempts < max_retry_attempts:
        retry_attempts += 1
        ws = None

        on_open(ws)
        print("retry_attempts: {}".format(retry_attempts))

    else:
        print("websocket closed by over max_retry_attempts: {}".format(retry_attempts))


if __name__ == "__main__":
    websocket.enableTrace(True)
    # host = "192.168.11.5:8080"
    host = "mugbot.herokuapp.com"
    scheme = "wss"
    ws = websocket.WebSocketApp(scheme + "://" + host + "/ws",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
