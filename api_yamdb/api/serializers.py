from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.core.validators import MinValueValidator, MaxValueValidator
from reviews.models import Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


class TitleGetSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = "__all__"
        model = Title


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    score = serializers.IntegerField(
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        )
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        user = self.context['request'].user
        if Review.objects.filter(title=title, author=user).exists():
            raise serializers.ValidationError(
                'Можно оставить только один отзыв'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
