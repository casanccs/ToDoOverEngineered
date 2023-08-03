from django.urls import path
from .views import *
urlpatterns = [
    path('', NotesList, name="NotesList"),
    path('note/<str:id>', NoteDetail, name='NoteDetail'),
    path('createNote/', CreateNote, name='CreateNote'),
    path('deleteNote/<str:id>', DeleteNote, name='DeleteNote'),
    path('createAccount/', CreateAccount, name='CreateAccount'),
    path('login/', Login, name='Login'),
    path('logout/', Logout, name='Logout'),
]
