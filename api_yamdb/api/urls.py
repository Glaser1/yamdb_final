
from django.urls import include, re_path, path
from rest_framework import routers
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from .views import AuthViewSet, ReviewViewSet, CommentViewSet
from .views import UserViewSet, CategoryViewSet, GenreViewSet, TitleViewSet


router1 = routers.DefaultRouter()
router1.register(r'v1/users', UserViewSet, basename='users')
router1.register(r'v1/auth', AuthViewSet, basename='auth')
router1.register(r'v1/categories', CategoryViewSet, basename='categories')
router1.register(r'v1/genres', GenreViewSet, basename='genres')
router1.register(r'v1/titles', TitleViewSet, basename='titles')
router1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    re_path('', include(router1.urls)),

    path('api/v1/token/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'
         ),
    path('api/v1/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'
         ),
    path('api/v1/api-token-auth/', views.obtain_auth_token),

]
