from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from .serializers import *
from .models import *
from django.middleware import csrf
import datetime
import jwt


def getUser(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated token!')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except:
        raise AuthenticationFailed('Unauthenticated!')
    user = User.objects.filter(id=payload['id']).first()
    return user

def login(user):
    payload = {
        'id': user.id,
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    response = Response()
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {'jwt': token}
    return response
# Create your views here.
class UserView(APIView):

    def post(self, request): # Mimic registering AND Logging in!
        form = request.data
        print(form)

        try:
            if form['iss']:
                # Must see if user exists already
                user = User.objects.filter(username=form['email']).first()
                if user:
                    response = login(user)
                    return response
                else:
                    user = User.objects.create(username=form['email'])
                    user.save()
                    response = login(user)
                    return response
        except:
            try:
                # Must check form here to ensure uniqueness, and correct format of username and password, otherwise move on
                user = User.objects.create_user(username=form['username'], password=form['password'])
                user.save()
                response = login(user)
                response.status_code = 201
                return response
            except:
                return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request): # Mimic logging in
        form = request.data
        user = authenticate(username=form['username'], password=form['password']) # Not sure if I should use this, but why not
        if user:
            response = login(user)
            return response
        return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request): # Mimic logging out
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Successfully Logged Out'
        }
        return response
    
    def get(self, request):
        user = getUser(request)
        serializer = UserSerializer(user)
        return Response(serializer.data)