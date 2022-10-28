import channels_graphql_ws
import graphene


class UserConfirm(channels_graphql_ws.Subscription):
    payload = graphene.Boolean()

    class Arguments:
        id = graphene.String(required=True)

    @staticmethod
    def subscribe(root, info, id):
        return [id] if id is not None else None

    @staticmethod
    def publish(payload, info, id):
        return UserConfirm(payload=payload)


class Subscription:
    user_confirm = UserConfirm.Field()
