from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from .serializers import *
from .models import *

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


class NotesList(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)
    
class NoteView(APIView):

    def get(self, request, id):
        if id == "new":
            return Response("Expecting New Instance")
        note = Note.objects.get(id=id)
        serializer = NoteSerializer(note, many=False)
        return Response(serializer.data)
    
    def post(self, request, id):
        form = request.data
        note = Note(title=form['title'], text=form['text'])
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