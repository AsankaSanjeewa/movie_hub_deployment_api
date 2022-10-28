from curses import meta

import channels_graphql_ws
import graphene

from .inputs import BookInput

from .models import Book
from .types import BookType


class NotifyTodo(channels_graphql_ws.Subscription):
    book = graphene.Field(BookType)
    payload = graphene.JSONString()
    username = graphene.String(required=True)

    class Arguments:
        username = graphene.String(required=True)

    @staticmethod
    def subscribe(root, info, username):
        return [username] if username is not None else None

    @staticmethod
    def publish(payload, info, username):
        return NotifyTodo(payload=payload, username=username)

class BookQuery:
    hello = graphene.String()
    all_books = graphene.List(BookType)
    book = graphene.Field(BookType, book_id=graphene.Int())

    def resolve_all_books(self, info, **kwargs):
        return Book.objects.all()

    def resolve_book(self, info, book_id):
        return Book.objects.get(pk=book_id)

    def resolve_hello(self, info, **kwargs):
        return "Hello"

class BookSubscription:
    notify_todo = NotifyTodo.Field()




class CreateBook(graphene.Mutation):
    class Arguments:
        book_data = BookInput(required=True)
    
    book = graphene.Field(BookType)

    @staticmethod
    def mutate(root, info, book_data=None):
        book_instance = Book(
            title = book_data.title,
            author = book_data.author,
            year_published = book_data.year_published,
            review = book_data.review
        )
        book_instance.save()
        NotifyTodo.broadcast(
            # Subscription group to notify clients in.
            group="test2",
            # Dict delivered to the `publish` method.
            payload=book_data,
        )
        return CreateBook(book=book_instance)

class UpdateBook(graphene.Mutation):
    class Arguments:
        book_data = BookInput(required=True)

    book = graphene.Field(BookType)

    @staticmethod
    def mutate(root, info, book_data=None):

        book_instance = Book.objects.get(pk=book_data.id)

        if book_instance:
            book_instance.title = book_data.title
            book_instance.author = book_data.author
            book_instance.year_published = book_data.year_published
            book_instance.review = book_data.review
            book_instance.save()

            return UpdateBook(book=book_instance)
        return UpdateBook(book=None)

class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    book = graphene.Field(BookType)

    @staticmethod
    def mutate(root, info, id):
        book_instance = Book.objects.get(pk=id)
        book_instance.delete()

        return None

class BookMutation:
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()


