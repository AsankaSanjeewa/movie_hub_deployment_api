from graphene_django import DjangoObjectType

from .models import Book


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "year_published", "review")
        # fields = "__all__"
