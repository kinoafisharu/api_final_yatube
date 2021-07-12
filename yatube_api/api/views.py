from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.utils.datastructures import MultiValueDict

from .models import Post, Follow, Group
from .serializers import CommentSerializer, PostSerializer, \
    FollowSerializer, GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = []

    def get_queryset(self):
        group_id = self.request.query_params.get("group")
        if group_id:
            posts = Post.objects.filter(group=group_id)
        else:
            posts = Post.objects.all()

        return posts

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.id != self.get_object().author_id:
            raise PermissionDenied

        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.id != instance.author_id:
            raise PermissionDenied

        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs['id'])
        queryset = post.comments.all()
        return queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['id'])
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        if self.request.user.id != self.get_object().author_id:
            raise PermissionDenied

        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.id != instance.author_id:
            raise PermissionDenied

        instance.delete()


@api_view(['GET', 'POST'])
def follow(request):
    if request.method == 'POST':
        data = MultiValueDict(request.data)
        data.update({'user': request.user.username})
        serializer = FollowSerializer(data=data)
        if serializer.is_valid():
            if Follow.objects.filter(user=request.user, following__username=data.get('following')).count():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            if data.get('following') == request.user.username:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    follows = Follow.objects.filter(following=request.user.id)

    filter_name = request.query_params.get("search")

    if filter_name:
        follows = follows.filter(user__username=filter_name)

    serializer = FollowSerializer(follows, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([])
def group(request):
    if request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    groups = Group.objects.all()
    serializer = GroupSerializer(groups, many=True)
    return Response(serializer.data)
