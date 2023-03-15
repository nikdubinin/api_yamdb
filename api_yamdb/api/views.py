from django.shortcuts import render

from rest_framework import filters, viewsets

from .mixins import CreateDestroyListViewSet
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer)
from reviews.models import Category, Genre, Title


class CategoryViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
