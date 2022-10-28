from dataclasses import field, fields
from pyexpat import model
from graphene_django import DjangoObjectType
from .models import ExtendUser
class ImageUploadType(DjangoObjectType):
    class Meta:
        model = ExtendUser
        field = "imageUrl"

class UserType(DjangoObjectType):
    class Meta:
        model = ExtendUser
        fields = ("id", "email")

        