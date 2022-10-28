import channels_graphql_ws
import graphene
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from src.apps.books.schema import BookMutation, BookQuery, BookSubscription
from src.apps.users.schema import UserMutation, UserQuery, UserSubscription


class Subscription(
    graphene.ObjectType,
    UserSubscription,
    BookSubscription
):
    pass

class Query(
    BookQuery,
    UserQuery
):
    pass

class Mutation(
    graphene.ObjectType, 
    BookMutation,
    UserMutation
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)

def my_middleware(next_middleware, root, info, *args, **kwds):
        """My custom GraphQL middleware."""
        # Invoke next middleware.
        print('My custom GraphQL middleware.')
        return next_middleware(root, info, *args, **kwds)
class MyGraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    """Channels WebSocket consumer which provides GraphQL API."""
    schema = schema

    # confirm_subscriptions=True

    # Uncomment to send keepalive message every 42 seconds.
    send_keepalive_every = 10

    # Uncomment to process requests sequentially (useful for tests).
    strict_ordering = False

    middleware = [my_middleware]

    async def on_connect(self, payload):
        """New client connection handler."""
        # You can `raise` from here to reject the connection.
        print(payload)
        print("New client connected!")

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("graphql",MyGraphqlWsConsumer.as_asgi()),
    ])
})



# aniso8601==7.0.0
# asgiref==3.5.2
# # backports.zoneinfo==0.2.1
# backports.zoneinfo;python_version<"3.9"
# Django==4.1
# graphene==2.1.9
# graphene-django==2.15.0
# graphql-core==2.3.2
# graphql-relay==2.0.1
# promise==2.3
# Rx==1.6.1
# singledispatch==3.7.0
# six==1.16.0
# sqlparse==0.4.2
# text-unidecode==1.3
# # Django>=3.0,<4.0
# psycopg2>=2.8
# django-environ==0.9.0

