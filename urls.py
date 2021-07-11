from django.urls import include, path
#from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, PostViewSet, FollowViewSet, GroupViewSet

"""
urlpatterns = [
    
    path("follow/", views.follow_index),
    path("follow/", views.follow_create),
    path("group/", views.groap_create),
    path("group/"), views.group_index),
    ]
"""

router = DefaultRouter()

router.register(
    'posts',
    PostViewSet,
    basename='posts')
router.register(
    'posts/(?P<id>.+)/comments',
    CommentViewSet,
    basename='comments')
router.register(
    'follow',
    FollowViewSet,
    basename='follow')
router.register(
    'group',
    GroupViewSet,
    basename='group')
    

urlpatterns = [
    
    # Djoser создаст набор необходимых эндпоинтов.
    # базовые, для управления пользователями в Django:
    path('auth/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('auth/', include('djoser.urls.jwt')),
]
