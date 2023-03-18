from django.shortcuts import get_object_or_404
from django.db.models import Avg

from rest_framework import filters, viewsets

from .mixins import CreateDestroyListViewSet
from .serializers import (CategorySerializer, GenreSerializer,
                          TitlePostSerializer, TitleGetSerializer,
                          ReviewSerializer, CommentSerializer)
from reviews.models import Category, Genre, Title, Review
from .permissions import (IsAuthorOrReadOnly, ReadOnly)


class CategoryViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (ReadOnly,)
    search_fields = ('name',)


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleGetSerializer
    permission_classes = (ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return TitlePostSerializer
        return TitleGetSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly,)

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
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
