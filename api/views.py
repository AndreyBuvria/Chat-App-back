from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate

from chatroom.models import Message, Room
from .serializers import MessagesSerializer
    
class Messages(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        print(request)
        room_name = Room.objects.get(name=pk)
        msgs = Message.objects.filter(room=room_name)
        serializer = MessagesSerializer(msgs, many=True)
        return Response(serializer.data)

class Login(APIView):
    def post(self, request):
        username = request.data['user']
        password = request.data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            token = Token.objects.get(user=user)
        else:
            return Response({'user': 'not found'})
        return Response({'token': token.key})