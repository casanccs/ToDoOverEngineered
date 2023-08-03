from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def NotesList(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Login'))
    profile = Profile.objects.get(user = request.user)
    notes = Note.objects.filter(profile=profile)

    context = {
        'notes': notes,
        'profile': profile,
    }

    return render(request, 'notesList.html', context)

def CreateNote(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Login'))
    if request.method == "GET":
        return render(request, 'createNote.html')
    if request.method == "POST":
        profile = Profile.objects.get(user = request.user)
        form = request.POST
        note = Note(profile=profile, title=form['title'], text=form['text'])
        note.save()
        return HttpResponseRedirect(reverse('NotesList'))

    


def NoteDetail(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Login'))
    note = Note.objects.get(id=id)
    profile = Profile.objects.get(user = request.user)
    if request.method == "GET":
        context = {
            'note': note,
            'profile': profile,
        }
        return render(request, 'noteDetail.html', context)
    if request.method == "POST":
        form = request.POST
        note.title = form['title']
        note.text = form['text']
        note.save()
        return HttpResponseRedirect(reverse('NotesList'))

    
def DeleteNote(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Login'))
    note = Note.objects.get(id=id)
    note.delete()
    return HttpResponseRedirect(reverse('NotesList'))

def CreateAccount(request):
    if request.method == "GET":
        return render(request, "createAccount.html")
    if request.method == "POST":
        form = request.POST
        user = User.objects.create_user(username=form['username'], password=form['password'])
        user.save()
        profile = Profile(user=user)
        profile.save()
        login(request, user)
        return HttpResponseRedirect(reverse('NotesList'))
    
def Login(request):
     if request.method == "GET":
        return render(request, "login.html")
     if request.method == "POST":
        form = request.POST
        print(form['username'], form['password'])
        user = authenticate(username=form['username'], password=form['password'])
        print(user)
        if user:
            login(request,user)
            return HttpResponseRedirect(reverse('NotesList'))
        else:
            return HttpResponseRedirect(reverse('Login'))
    
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login'))