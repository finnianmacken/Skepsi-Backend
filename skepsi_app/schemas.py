import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from django.db.models import Count
from django.utils.text import slugify

from .models import User, Topic, Paper, Annotation, Reference, Score, ScoreChoices, Figure, Profile

from .auth0 import delete_user

from .tasks import classify_topics_queue_manager

import json
import jwt
import requests
import environ

from django.db.models import Count

env = environ.Env()
environ.Env.read_env()

################### JWT PARSING #############################

def jwt_decode_token(info):
    token = info.context.META.get('HTTP_AUTHORIZATION')
    print(info.context.META) # DEBUG
    header = jwt.get_unverified_header(token)
    jwks = requests.get('https://{}/.well-known/jwks.json'.format('skepsi.us.auth0.com')).json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    issuer = 'https://{}/'.format('skepsi.us.auth0.com')
    decoded_token = jwt.decode(token, public_key, audience=env("TOKEN_AUDIENCE"), issuer=issuer, algorithms=['RS256'])
    return decoded_token


def extract_token_permissions(info):
    decoded_token = jwt_decode_token(info)
    permissions = decoded_token.get('permissions')
    return permissions



######f############# QUERIES #############################


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = "__all__"

class TopicType(DjangoObjectType):
    class Meta:
        model = Topic
        fields = '__all__'

    paper_count = graphene.Int()
    annotation_count = graphene.Int()
    scientist_count = graphene.Int()

    def resolve_paper_count(self, info):
        return self.papers.count()

    def resolve_annotation_count(self, info):
        return Paper.objects.filter(topic__header=self.header).aggregate(Count('annotations'))['annotations__count']

    def resolve_scientist_count(self, info):
        sum = 0
        paper_qs = Paper.objects.filter(topic__pk=self.id)
        for paper in paper_qs:
            scientist_set = set()
            annotation_qs = Annotation.objects.filter(paper__pk=paper.id)
            for annotation in annotation_qs:
                user_qs = User.objects.filter(annotations__pk=annotation.id)
                for user in user_qs:
                    scientist_set.add(user.username)
            sum += len(scientist_set)
        return sum

class PaperType(DjangoObjectType):
    class Meta:
        model = Paper
        fields = '__all__'

    annotation_count = graphene.Int()
    reading_time = graphene.Int()
    scientist_count = graphene.Int()

    def resolve_annotation_count(self, info):
        return self.annotations.count()

    def resolve_reading_time(self, info):
        return round(len(self.md)/900)

    def resolve_scientist_count(self, info):
        scientist_set = set()
        annotation_qs = Annotation.objects.filter(paper__pk=self.id)
        for annotation in annotation_qs:
            user_qs = User.objects.filter(annotations__pk=annotation.id)
            for user in user_qs:
                scientist_set.add(user.username)
        return len(scientist_set)


class ReferenceType(DjangoObjectType):
    class Meta:
        model = Reference
        fields = "__all__"


class FigureType(DjangoObjectType):
    class Meta:
        model = Figure
        fields = "__all__"


class AnnotationType(DjangoObjectType):
    class Meta:
        model = Annotation
        fields = '__all__'

    child_annotation_count = graphene.Int()

    def resolve_child_annotation_count(self, info):
        return self.children.count()


class ScoreType(DjangoObjectType):
    class Meta:
        model = Score
        fields = "__all__"


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)

    user_by_username = graphene.Field(UserType, username=graphene.String())

    all_topics = graphene.List(TopicType)

    all_papers = graphene.List(PaperType)
    papers_by_topic = graphene.Field(lambda: graphene.List(PaperType),
                                     slug=graphene.String())
    papers_by_id = graphene.Field(PaperType,
                                 paper_id = graphene.ID())

    references_by_paper_id = graphene.Field(lambda: graphene.List(ReferenceType),
                                            paper_id = graphene.ID())

    all_annotations = graphene.List(AnnotationType)

    annotations_by_author = graphene.Field(lambda: graphene.List(AnnotationType),
                                           username=graphene.String())
    annotations_by_id = graphene.Field(lambda: graphene.List(AnnotationType),
                                       id=graphene.ID())
    annotations_by_paper_id = graphene.Field(lambda: graphene.List(AnnotationType),
                                             paper_id=graphene.ID())

    scores_by_paper_id = graphene.Field(lambda: graphene.List(ScoreType),
                                        paper_id=graphene.ID())
    # TODO: need to use username here, but can't configure until the interface for
    # user manipulation is finished
    # def resolve_all_annotations(root, info):
    #     permissions = extract_token_permissions(info)
    #     if permissions.count('read:all_annotations') > 0:
    #         return Annotation.objects.select_related('document').select_related('user').all()
    #     else:
    #         return Annotation.objects.select_related('document').select_related('user').get(user=info.context.user)

    # def resolve_all_papers(root, info):
    #     permissions = extract_token_permissions(info)
    #     if permissions.count('read:document_1') > 0:
    #         return Document.objects.filter(title='document_1')
    #     else:
    #         return Document.objects.all()

    def resolve_all_users(root, info):
        return User.objects.all()

    def resolve_all_topics(root, info):
        return Topic.objects.all()

    def resolve_all_papers(root, info):
        return Paper.objects.all()

    def resolve_papers_by_topic(root, info, slug):
        return Paper.objects.filter(topic__slug__contains=slug)

    def resolve_papers_by_id(root, info, paper_id):
        return Paper.objects.get(pk=paper_id)

    def resolve_references_by_paper_id(root, info, paper_id):
        return Reference.objects.filter(paper__pk=paper_id)

    def resolve_all_annotations(root, info):
        return Annotation.objects.all()

    def resolve_annotations_by_author(root, info, username):
        return Annotation.objects.filter(author__username__contains=username)

    def resolve_annotations_by_id(root, info, id):
        return Annotation.objects.filter(id=id)

    def resolve_annotations_by_paper_id(root, info, paper_id):
        return Annotation.objects.filter(paper__pk=paper_id)

    def resolve_user_by_username(root, info, username):
        return User.objects.get(username=username)

    def resolve_scores_by_paper_id(root, info, paper_id):
        return Score.objects.filter(annotation__paper__pk=paper_id)


################### MUTATIONS #############################


class UserInputType(graphene.InputObjectType):
    username = graphene.String()
    password = graphene.String()
    email = graphene.String(required=True)
    domains = graphene.String()


class AnnotationInput(graphene.InputObjectType):
    author = graphene.String()
    quote = graphene.String()
    content = graphene.String()
    id = graphene.ID()


class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = UserInputType()

    user = graphene.Field(UserType)

    def mutate(root, info, user_data):
        user = User(
            username=user_data.username,
            email=user_data.email,
        )
        user.set_password(user_data.password)
        user.save()
        profile = Profile(user=user, domains=user_data.domains)
        profile.save()
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    class Arguments:
        user_data = UserInputType(required=True)

    user = graphene.Field(lambda: UserType)

    # TODO: need to use id here, but can't configure until the interface for
    # user manipulation is finished
    def mutate(root, info, user_data=None):
        user = User.objects.get(username=user_data.username)
        user.email = user_data.email
        user.password = user_data.password
        user.save()
        return UpdateUser(user=user)

# TODO: UpdateUser is still in jwt_test -- get it later


class DeleteUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)
        email = graphene.String(required=True)

    done = graphene.Boolean()

    def mutate(root, info, user_id, email):
        delete_user(user_id)
        user = User.objects.get(email=email)
        user.delete()
        return DeleteUser(done=True)


class CreateAnnotation(graphene.Mutation):
    class Arguments:
        author = graphene.String(required=True)
        content = graphene.String(required=True)
        quote = graphene.String()
        paperId = graphene.ID(required=True)
        start = graphene.Int()
        stop = graphene.Int()
        parentId = graphene.ID()

    annotation = graphene.Field(AnnotationType)

    def mutate(root, info, author, content, quote, paperId, start, stop, parentId):
        annotation = Annotation(
            paper=Paper.objects.get(pk=paperId),
            author=User.objects.get(username=author),
            content=content,
            quote=quote,
            start=start,
            stop=stop
            )
        print("PARENT ID", parentId)
        if(parentId):
            annotation.parent = Annotation.objects.get(pk=parentId)
        annotation.save()
        # classify_topics_queue_manager.delay(content, annotation.id)
        return CreateAnnotation(annotation=annotation)


class UpdateAnnotation(graphene.Mutation):
    class Arguments:
        annotation_data = AnnotationInput(required=True)

    annotation = graphene.Field(AnnotationType)

    def mutate(root, info, annotation_data):
        annotation = Annotation.objects.get(id=annotation_data.id)

        if annotation_data.quote != '':
            annotation.quote = annotation_data.quote
        if annotation_data.content != '':
            annotation.content = annotation_data.content
        annotation.save()
        return UpdateAnnotation(annotation=annotation)


class DeleteAnnotation(graphene.Mutation):
    class Arguments:
        annotationId = graphene.ID(required=True)

    annotation = graphene.Field(AnnotationType)

    def mutate(root, info, annotationId):
        annotation = Annotation.objects.get(id=annotationId)
        annotation.delete()
        return DeleteAnnotation(annotation=annotation)


class SoftDeleteAnnotation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    annotation = graphene.Field(AnnotationType)

    def mutate(root, info, annotation_data):
        annotation = Annotation.objects.get(id=id)
        annotation.content = '[deleted]'
        annotation.save()
        return SoftDeleteAnnotation(annotation=annotation)


class CreateScore(graphene.Mutation):
    class Arguments:
        annotation_id = graphene.ID(required=True)
        scoreNumber = graphene.Int(required=True)
        explanation = graphene.String()
        field = graphene.String()

    score = graphene.Field(ScoreType)

    def mutate(root, info, annotation_id, scoreNumber, explanation, field):
        score = Score(
            scoreNumber=scoreNumber,
            annotation=Annotation.objects.get(id=annotation_id),
            explanation=explanation,
            field=field
        )
        score.save()
        return CreateScore(score=score)


class UpdateScore(graphene.Mutation):
    class Arguments:
        scoreId = graphene.ID(required=True)
        explanation = graphene.String()
        scoreNumber = graphene.Int()
        field = graphene.String()

    score = graphene.Field(ScoreType)

    def mutate(root, info, scoreId, explanation, scoreNumber, field):
        print("THIS IS INFO:", scoreId, explanation, scoreNumber, field)
        score = Score.objects.get(pk=scoreId)
        score.explanation = explanation
        score.scoreNumber = scoreNumber
        score.field = field
        score.save()
        return UpdateScore(score=score)

class DeleteScore(graphene.Mutation):
    class Arguments:
        scoreId = graphene.ID(required=True)

    score = graphene.Field(ScoreType)

    def mutate(root, info, scoreId):
        score = Score.objects.get(pk=scoreId)
        score.delete()
        return DeleteScore(score=score)


class CheckUserExists(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    exists = graphene.Boolean()

    @staticmethod
    def mutate(root, info, username):
        user = User.objects.get(username=username)
        print(f'User {user.username} does exist')
        return CheckUserExists(exists=True)


class CheckEmailExists(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)

    exists = graphene.Boolean()

    @staticmethod
    def mutate(root, info, email):
        user = User.objects.get(email=email)
        print(f'User with email {user.email} does exist')
        return CheckEmailExists(exists=True)


class PlaceholderMutation(graphene.Mutation):
    class Arguments:
        placeholder_field = graphene.String()

    score = graphene.Field(ScoreType)

    def mutate(root, info, placeholder_field):
        pass


class Mutations(graphene.ObjectType):
    create_annotation = CreateAnnotation.Field()
    update_annotation = UpdateAnnotation.Field()
    delete_annotation = DeleteAnnotation.Field()
    soft_delete_annotation = SoftDeleteAnnotation.Field()
    create_score = CreateScore.Field()
    update_score = UpdateScore.Field()
    delete_score = DeleteScore.Field()
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    check_user_exists = CheckUserExists.Field()
    check_email_exists = CheckEmailExists.Field()
    delete_user = DeleteUser.Field()
    placeholder_mutation = PlaceholderMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutations)
