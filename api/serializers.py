from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.models import Title, Category, Genre, Review, Comment

User = get_user_model()


class CategoryField(serializers.RelatedField):

    default_error_messages = {
        'incorrect_type': 'Incorrect type. Expected a string but got {input_type}.',
        'does_not_exist': 'Category slug ({slug}) does not exist in database.'
    }

    def get_queryset(self):
        return Category.objects.all()

    def to_internal_value(self, data):
        if not isinstance(data, str):
            self.fail('incorrect_type', input_type=type(data).__name__)

        qs = self.get_queryset()
        exist = qs.filter(slug=data).exists()
        if not exist:
            self.fail('does_not_exist', slug=data)

        return qs.get(slug=data)

    def to_representation(self, value):
        return CategorySerializer(value).data


class GenreField(serializers.RelatedField):

    default_error_messages = {
        'incorrect_type': 'Incorrect type. Expected string but got {input_type}.',
        'does_not_exist': 'Genre ({slug}) does not exist in database.'
    }

    def get_queryset(self):
        return Genre.objects.all()

    def to_internal_value(self, data):
        if not isinstance(data, str):
            self.fail('incorrect_type', input_type=type(data).__name__)

        qs = self.get_queryset()
        genres_qs = qs.values_list('slug', flat=True)
        if data not in genres_qs:
            self.fail('does_not_exist', slug=data)

        return qs.get(slug=data)

    def to_representation(self, value):
        return GenreSerializer(value).data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'slug']


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryField(many=False)
    genres = GenreField(many=True)

    class Meta:
        model = Title
        fields = ['id', 'title', 'year', 'category', 'genres']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'score', 'pub_date']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'pub_date']


class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name',
            'bio', 'email', 'role'
        ]


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name',
            'bio', 'email', 'role'
        ]


class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class UserConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)
