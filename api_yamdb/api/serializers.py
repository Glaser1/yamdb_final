from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title
from reviews.models import User
from reviews.models import Review, Comment


class GetTitle:
    requires_context = True

    def __call__(self, serializer_field):
        c_view = serializer_field.context['view']
        title_id = c_view.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
    title = serializers.HiddenField(default=GetTitle())

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'pub_date', 'score', 'title')
        validators = (
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author',)
            ),
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class AuthTokenSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class AuthSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=None,
        min_length=None,
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                ('Нельзя создвать пользователя с username = me')
            )
        return value


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=None,
        min_length=None,
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    role = serializers.ChoiceField(
        default=User.USER,
        choices=User.ROLE_CHOICES
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'first_name',
                  'last_name', 'bio')

    def validate_role(self, value):
        role = self.context['request'].user.role
        if role == User.USER and role != value:
            value = User.USER
        return value


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Категорий"""
    slug = serializers.SlugField(
        required=True,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )
    name = serializers.CharField(required=True)

    class Meta:
        exclude = ('id',)
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Жанров"""

    class Meta:
        exclude = ('id',)
        model = Genre
        lookup_field = 'slug'


class TitleListSerializer(serializers.ModelSerializer):
    """Серилализатор для GET запросов модели Title"""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для POST запросов модели Title"""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title
