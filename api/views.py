from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status

from django.contrib.auth import authenticate, login

from chatroom.models import Message, Room
from .serializers import MessagesSerializer, RoomsSerializer
    
class Messages(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        room_name = Room.objects.get(id=pk)
        msgs = Message.objects.filter(room=room_name)
        serializer = MessagesSerializer(msgs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Rooms(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomsSerializer(rooms, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Login(APIView):
    def post(self, request):
        username = request.data['user']
        password = request.data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)

        else:
            return Response({'Auth': 'Incorrect credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({
            'token': token.key, 
            'user': request.user.username}, status=status.HTTP_200_OK)