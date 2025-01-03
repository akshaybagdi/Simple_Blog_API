from rest_framework import serializers
from ..models.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    # author_name = serializers.CharField(source='author.username')
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']
