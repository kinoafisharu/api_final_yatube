from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, PostViewSet
from . import views

router = DefaultRouter()

router.register(
    'posts',
    PostViewSet,
    basename='posts')
router.register(
    'posts/(?P<id>.+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    # Djoser создаст набор необходимых эндпоинтов.
    # базовые, для управления пользователями в Django:
    path('auth/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('auth/', include('djoser.urls.jwt')),

    path('follow/', views.follow),
    path('group/', views.group)
] + router.urls
