from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .models import User
from .serializers import UserSerializer

# Create your views here.
class UserViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=False)
    def update_user(self, request):
        user_id = request.GET.get('id')
        payment = request.GET.get('payment')
        action = request.GET.get('action')

        if not user_id or not payment or not action:
            return Response({'error': 'dont find parametrs'})

        try:
            user_id = int(user_id)
        except:
            return Response({'error': 'id not is int'})

        try:
            payment = int(payment)
        except:
            return Response({'error': 'payment not is int'})

        try:
            user = User.objects.get(id=user_id)
        except:
            return Response({'error': 'not user with this id'})

        if action == 'p':
            user.cash += payment   
        elif action == 'm':
            user.cash -= payment
        else:
            return Response({'error': 'action dont p(plus) or m(minus)'})    
        
        user.save() 

        return Response({'name':user.name, 'updated cash': user.cash})
