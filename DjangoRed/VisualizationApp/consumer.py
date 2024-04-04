import json
from channels.generic.websocket import WebsocketConsumer

class ClusterConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
                'type':'connection_established',
             'message': "Connected"
            }
        ))
    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
    def disconnect(self, close_code):
        print(close_code)