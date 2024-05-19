import json
import base64
from channels.generic.websocket import WebsocketConsumer
from wordcloud import WordCloud
import io
from PIL import Image

from IdApp.db_query import execute
from DjangoRed.settings import NATIVE_SQL_DATABASES

class StatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
                'type':'connection_established',
                'message': "Consumer info of Connection"
            }
        ))

    def receive(self, text_data=None, bytes_data=None):
        received_message = json.loads(text_data)
        submissonNames = received_message["names"]
        #try:

        f_query = """ SELECT st.word_cloud, st.full_name, st.upvote
                  FROM statisticsdb.statistic AS st
                  WHERE st.full_name {in_expr}
                  ORDER BY st.upvote
                  DESC; """

        in_expr = "IN ( "
        params = {}
        wrapped = []
        for s in submissonNames:
            params[s] = s
            wrapped.append(f"%({s})s")

        in_expr += ", ".join(wrapped) +" )"

        query = f_query.format(in_expr = in_expr)
        print(query)

        table_data = execute(NATIVE_SQL_DATABASES['stat'], query, params)
        test_message_back = []
        for i in table_data:
            test_message_back.append(str(i[0])[2:-1])
        
        self.send(text_data=json.dumps({
            "type": "info",
            "info": test_message_back,
            }))

    def disconnect(self, close_code):
        print(close_code)
    