import json
import graphene
from graphene_file_upload.scalars import Upload

class Query(graphene.ObjectType):

    name = graphene.String(suffix=graphene.String())
    headers = graphene.String()

    def resolve_name(self, info, **kwargs):
        return "The Republic of Heaven" + kwargs.get("suffix", "")


    def resolve_headers(self, info, **kwargs):
        return ", ".join([
            h for h in sorted(info.context.META) if h.startswith("HTTP")
        ])


class UploadImageMutation(graphene.Mutation):

    class Arguments:
        image = Upload()

    information = graphene.String()

    def mutate(self, info, **kwargs):
        return UploadImageMutation(information=str(kwargs))



class Mutation(graphene.ObjectType):
    upload_image = UploadImageMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
