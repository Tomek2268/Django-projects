from rest_framework import serializers

from ..models import TicTacToeGame

class TicTacToeGameSerializer(serializers.ModelSerializer):

    class Meta:
        model = TicTacToeGame
        fields = '__all__'