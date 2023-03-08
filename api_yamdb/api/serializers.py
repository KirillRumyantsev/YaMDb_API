import datetime as dt

from django.db.models import Avg
from rest_framework import serializers

from reviews.models import (Category, Comment, Genre, GenreTitle,
                            Review, Title, User)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError('Имя me не допустимо')
        elif username is None or username == "":
            raise serializers.ValidationError('Заполните поле имя')
        return username

    def validate_email(self, email):
        if email is None or email == "":
            raise serializers.ValidationError('Заполните поле email')
        return email


class AuthentificationSerializer(serializers.Serializer):
    username = serializers.RegexField(
        max_length=150,
        regex=r"^[\w.@+-]+\Z",
        required=True
    )
    email = serializers.EmailField(
        max_length=254,
        required=True
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Имя "me" запрещено.')
        return value

    def validate(self, data):
        if User.objects.filter(username=data.get('username'),
                               email=data.get('email')).exists():
            return data
        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError(
                f'Пользователь с таким именем {data} уже существует.'
            )
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError(
                f'Пользователь с таким email: {data} уже существует.'
            )
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=100, required=True)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, required=True)
    rating = serializers.SerializerMethodField()
    category = CategorySerializer()
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        result = Title.objects.aggregate(rating=Avg('reviews__score'))
        return result['rating']


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug', many=True,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    description = serializers.CharField(
        required=False
    )

    class Meta:
        model = Title
        fields = (
            'name', 'year', 'description', 'genre', 'category'
        )

    def validate_year(self, value):
        if value > dt.date.today().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True)
    score = serializers.IntegerField(required=True)
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True)
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
