from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .mixins import CustomMixin
from .pagination import UsersPagination
from .permissions import (AdminUser, AuthorOrStaff, IsAdminOrReadOnly,
                          UserReadOnly)
from .serializers import (AuthSerializer, AuthTokenSerializer,
                          CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleListSerializer,
                          UserSerializer)


class AuthViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AuthSerializer
    permission_classes = (permissions.AllowAny,)

    @action(methods=['post'], detail=False)
    def signup(self, request, pk=None):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            user = User(username=request.data['username'],
                        email=request.data['email'])
            user.confirmation_code = default_token_generator.make_token(user)
            user.save()
            send_mail(
                'Confirmation code',
                user.confirmation_code,
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            return Response({'username': user.username, 'email': user.email})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def token(self, request, pk=None):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, username=request.data['username'])
            if user.confirmation_code != request.data['confirmation_code']:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UsersPagination
    lookup_field = 'username'
    permission_classes = (permissions.IsAuthenticated, UserReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        if kwargs['username'] == 'me':
            user = request.user
        else:
            user = get_object_or_404(
                self.queryset,
                username=kwargs['username']
            )
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        if kwargs['username'] == 'me':
            self.kwargs['username'] = request.user.username
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if kwargs['username'] == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CategoryViewSet(CustomMixin):
    """Получить список всех категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'create' or self.action == 'destroy':
            return permissions.IsAuthenticated(), AdminUser(),
        return super().get_permissions()


class GenreViewSet(CustomMixin):
    """Получить список всех жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = ()
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'create' or self.action == 'destroy':
            return permissions.IsAuthenticated(), AdminUser(),
        return super().get_permissions()


class TitleViewSet(ModelViewSet):
    """Получить список всех объектов"""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).all().order_by('-name')
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleListSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AuthorOrStaff,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AuthorOrStaff,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
