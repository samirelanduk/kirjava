import graphene

class Query(graphene.ObjectType):

    name = graphene.String()

    def resolve_name(self, info, **kwargs):
        return "The Republic of Heaven"

schema = graphene.Schema(query=Query)
