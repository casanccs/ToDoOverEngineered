from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from .serializers import *
from .models import *
from django.middleware import csrf

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
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        # Errors here because user is not authorized
        try:
            notes = Note.objects.filter(user=request.user)
            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Not Logged In", status=status.HTTP_401_UNAUTHORIZED)
    
class NoteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        if id == "new":
            return Response("Expecting New Instance")
        note = Note.objects.get(id=id, user=request.user)
        serializer = NoteSerializer(note, many=False)
        return Response(serializer.data)
    
    def post(self, request, id):
        form = request.data
        note = Note(title=form['title'], text=form['text'], user=request.user)
        note.save()
        return Response("Created Note Successfully!!")
    
    def put(self, request, id):
        note = Note.objects.get(id=id)
        form = request.data
        note.title = form['title']
        note.text = form['text']
        note.save()
        return Response("Updated Note Successfully!!")
    
    def delete(self, request, id):
        note = Note.objects.get(id=id)
        note.delete()
        return Response("Deleted Note Successfully!!")
    

class UserView(APIView):

    def post(self, request): # Mimic registering
        form = request.data
        # Must check form here to ensure uniqueness, and correct format of username and password, otherwise move on
        try:
            user = User.objects.create_user(username=form['username'], password=form['password'])
            user.save()
            login(request, user)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request): # Mimic logging in
        form = request.data
        print(form)
        user = authenticate(username=form['username'], password=form['password'])
        print(user)
        if user:
            login(request, user)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request): # Mimic logging out
        logout(request)
        return Response("Logged out",  status=status.HTTP_200_OK)
    
    def get(self, request): # Get user data, user should only be able to do this if they are authenticated
        serializer = UserSerializer(request.user)
        return Response(serializer.data)