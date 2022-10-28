from graphql_auth.schema import MeQuery, UserQuery


class Query(UserQuery, MeQuery):
    pass
