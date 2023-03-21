from rest_framework import serializers, validators
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from reviews.models import Category, Genre, Title, Review, Comment
from users.validators import validate_username

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre


class TitleGetSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(required=False)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = "__all__"
        model = Title
        read_only_fields = (
            'id', 'name', 'year', 'description', 'genre', 'category', 'rating'
        )


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.IntegerField(required=False)

    class Meta:
        fields = '__all__'
        model = Title
        read_only_fields = ('id', 'rating')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )
    score = serializers.IntegerField(
        min_value=settings.MIN_SCORE, max_value=settings.MAX_SCORE
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)

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
    review = serializers.ReadOnlyField(
        source='review.id'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        max_length=150,
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all(),
            ),
            validate_username
        ]
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            ),
        ]


class SignUpSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[validate_username]
    )


class ConfirmationSerializer(serializers.Serializer):

    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[validate_username]
    )
    confirmation_code = serializers.CharField(required=True, max_length=150)
