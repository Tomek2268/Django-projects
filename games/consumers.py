import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
#from channels_presence.models import Room
#from channels_presence.decorators import remove_presence

from .models import TicTacToeGame

class GameConsumer(WebsocketConsumer):
    def connect(self):

        self.room = self.scope['url_route']['kwargs']['room']
        self.room_group_name = f'{self.room}_room'
        #Room.objects.add(f'{self.room_group_name}',self.channel_name,self.scope['user'])

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
    
    #@remove_presence
    def disconnect(self, close_code):
        game = TicTacToeGame.objects.filter(room=self.room)
        user = self.scope['user']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'user_left',
                'user':user.username
            }
        )

        if game:
            game = game[0]
            if game.host == user:
                game.delete()
            elif game.invited == user:
                game.invited = None
                game.save()

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        mark = text_data_json.get('mark')
        spot = text_data_json.get('spot')
        user = text_data_json.get('user')

        if spot:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'game_move',
                    'mark': mark,
                    'spot': spot
                }
            )

        if user:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'user_joined',
                    'user': user
                }
            )



    def game_move(self,event):
        mark = event['mark']
        spot = event['spot']

        self.send(text_data=json.dumps({
            'type':'player_move',
            'mark':mark,
            'spot':spot
        }))
    
    def user_joined(self,event):
        user = event['user']

        self.send(text_data=json.dumps({
            'type':'user_joined',
            'user':user
        }))

    def user_left(self,event):
        user = event['user']

        self.send(text_data=json.dumps({
            'type':'user_left',
            'user':user
        }))