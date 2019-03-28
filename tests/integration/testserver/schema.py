import graphene

class Query(graphene.ObjectType):

    name = graphene.String(suffix=graphene.String())
    headers = graphene.String()

    def resolve_name(self, info, **kwargs):
        return "The Republic of Heaven" + kwargs.get("suffix", "")


    def resolve_headers(self, info, **kwargs):
        return ", ".join([
         h for h in sorted(info.context.META) if h.startswith("HTTP")
        ])


schema = graphene.Schema(query=Query)
