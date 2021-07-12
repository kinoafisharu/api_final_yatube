from rest_framework import serializers

from .models import Comment, Post, Follow, Group


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True, )
    following = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True, )

    class Meta:
        fields = ("user", "following")
        model = Follow


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("title", "slug", "description")
        model = Group
