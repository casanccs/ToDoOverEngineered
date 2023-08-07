from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
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

@api_view()
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Returns list of all Note objects'
        },
        {
            'Endpoint': '/note/<id>',
            'method': 'GET',
            'body': None,
            'description': 'Returns single Note object'
        },
        {
            'Endpoint': '/note/new',
            'method': 'POST',
            'body': {'title': "", 'text': ""},
            'description': 'Creates new Note object'
        },
        {
            'Endpoint': '/note/<id>',
            'method': 'PUT',
            'body': {'title': "", 'text': ""},
            'description': 'Updates Note object with corresponding id'
        },
        {
            'Endpoint': '/note/<id>',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes Note object with corresponding id'
        },
    ]
    return Response(routes) # Needs safe=False because routes is a list, not a dictionary

@api_view()
def get_csrf_token(request):
    return Response({'csrfToken': csrf.get_token(request)})

class NotesList(APIView):

    def get(self, request):
        user = getUser(request)
        try:
            notes = Note.objects.filter(user=user)
            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Not Logged In", status=status.HTTP_401_UNAUTHORIZED)
    
class NoteView(APIView):

    def get(self, request, id):
        user = getUser(request)
        note = Note.objects.get(id=id, user=user)
        if id == "new":
            return Response("Expecting New Instance")
        serializer = NoteSerializer(note, many=False)
        return Response(serializer.data)
    
    def post(self, request, id):
        user = getUser(request)
        form = request.data
        note = Note(title=form['title'], text=form['text'], user=user)
        note.save()
        return Response("Created Note Successfully!!")
    
    def put(self, request, id):
        user = getUser(request)
        note = Note.objects.get(id=id)
        if user == note.user:
            form = request.data
            note.title = form['title']
            note.text = form['text']
            note.save()
            return Response("Updated Note Successfully!!")
        else:
            return Response("Unauthorized!", status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, id):
        user = getUser(request)
        note = Note.objects.get(id=id)
        if user == note.user:
            note.delete()
            return Response("Deleted Note Successfully!!")
        else:
            return Response("Unauthorized!", status=status.HTTP_401_UNAUTHORIZED)
    

class UserView(APIView):

    def post(self, request): # Mimic registering AND Logging in!
        form = request.data
        # Must check form here to ensure uniqueness, and correct format of username and password, otherwise move on
        try:
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