from rest_framework import serializers
# from simple_blog.posts.models.models import Post
from ..models.models import Post


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.StringRelatedField(source='author', read_only=True)
    # comments = CommentSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'abstract', 'content', 'author', 'author_name', 'publication_date', 'status',
                  'journal', 'volume', 'website', 'comments']
        read_only_fields = ['id', 'author', 'publication_date']

    def get_comments(self, obj):
        comments_qs = obj.comments.all()
        if comments_qs.exists():
            return [{"content": comment.content, "author_name": comment.author.username} for comment in comments_qs]
        return "This Post Have No Comment"
