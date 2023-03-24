from django.conf import settings
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.serializers import ValidationError

from .filters import TitleFilter
from .mixins import CreateDestroyListViewSet
from .permissions import IsAdminModeratorAuthor, IsAdmin, ReadOnly
from .serializers import (
    CategorySerializer, GenreSerializer,
    TitlePostSerializer, TitleGetSerializer,
    ReviewSerializer, CommentSerializer,
    SignUpSerializer, ConfirmationSerializer,
    UserSerializer, NotAdminUserSerializer, User
)
from reviews.models import Category, Genre, Title, Review


class CatogoryGenreBaseViewSet(CreateDestroyListViewSet):
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CatogoryGenreBaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CatogoryGenreBaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleGetSerializer
    permission_classes = (ReadOnly | IsAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitlePostSerializer
        return TitleGetSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthor,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthor,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdmin,
    )
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    http_method_names = ('post', 'get', 'patch', 'delete')
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )

    @action(
        methods=['patch', 'get'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(self.request.user)
        else:
            serializer = NotAdminUserSerializer(
                self.request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_confirmation_code(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(
            username=serializer.validated_data.get('username'),
            email=serializer.validated_data.get('email')
        )
    except IntegrityError:
        raise ValidationError(
            'Этот логин или email уже занят!'
        )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения: {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [serializer.validated_data.get('email')]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = ConfirmationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    confirmation_code = serializer.validated_data['confirmation_code']
    if not default_token_generator.check_token(user, confirmation_code):
        raise ValidationError(
            {'Неверный код подтверждения'}
        )
    token = AccessToken.for_user(user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)
