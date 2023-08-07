from rest_framework.serializers import ModelSerializer
from .models import *
from django.contrib.auth.models import User


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']