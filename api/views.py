from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView, RetrieveUpdateAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.filters import TitleFilter
from api.models import Title, Genre, Category, Review, User, Comment
from api.permissions import IsAdmin, GeneralPermission, IsStuff, IsOwner
from api.serializers import (
    TitleSerializer, GenreSerializer, CategorySerializer,
    UserAuthSerializer, UserConfirmationSerializer, UserCreateSerializer,
    UserUpdateSerializer, ReviewSerializer, CommentSerializer
)
from api.services import (
    get_tokens_for_user, send_email_to_user,
    validate_serializer, generate_confirmation_code, check_confirmation_code
)


@api_view(['POST'])
def email_auth(request):
    serializer = validate_serializer(UserAuthSerializer, request.data)

    email = serializer.data['email']
    confirmation_code = generate_confirmation_code(email)

    send_email_to_user(email, confirmation_code)

    return Response({
        'message': f'Your confirmation code was sent to {email}'
    })


@api_view(['POST'])
def user_auth(request):
    serializer = validate_serializer(UserConfirmationSerializer, request.data)

    email = serializer.data['email']
    code = serializer.data['confirmation_code']
    user, valid = check_confirmation_code(email, code)

    if not valid:
        return Response({
            'errors': 'Invalid confirmation code'
        }, status=status.HTTP_400_BAD_REQUEST)

    token = get_tokens_for_user(user)
    return Response(token)


class Titles(ListCreateAPIView):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = [GeneralPermission]


class TitleDetail(RetrieveUpdateDestroyAPIView):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [GeneralPermission]


class Genres(ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = [GeneralPermission]


class GenreDetail(DestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = [GeneralPermission]


class Categories(ListCreateAPIView, DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [GeneralPermission]


class CategoryDetail(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [GeneralPermission]


class Users(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated & IsAdmin]


class UserDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'email'
    permission_classes = [IsAuthenticated & IsAdmin]


class UserProfile(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.get_queryset().get(email=self.request.user.email)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user = self.get_queryset().get(email=self.request.user.email)
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Reviews(ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id)


class ReviewDetail(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated & (IsOwner | IsStuff)]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Review.objects.filter(pk=review_id)


class Comments(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comment.objects.filter(review_id=review_id)


class CommentDetail(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated & (IsOwner | IsStuff)]

    def get_queryset(self):
        comment_id = self.kwargs.get('comment_id')
        return Comment.objects.filter(pk=comment_id)









