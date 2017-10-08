import json
import websocket
import threading
import time

class Nasdaq(object):

    def __init__(self, symbol):
        self.mock_data = []

        self.symbol = symbol

        url = 'ws://34.214.11.52/stream?symbol={}'.format(symbol)
        ws = websocket.WebSocketApp(url,
                                    on_message = self.on_message,
                                    on_error = self.on_error,
                                    on_close = self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()


    def on_message(self, ws, message):
        self.mock_data.append(message)


    @staticmethod
    def on_error(ws, error):
        print(error)


    @staticmethod
    def on_close(ws):
        pass


    @staticmethod
    def on_open(ws):
        def run():
            ws.send("")
            time.sleep(1)
            ws.close()
        threading.Thread(target=run).start()


def simulate_data(symbol):
    return 'heyo'
    data = Nasdaq(symbol).mock_data
    pairs = []
    for line in data:
        line = json.loads(line)
        pairs.append([line["DateStamp"], line["LastSale"]])
    return str({"apple": pairs})
