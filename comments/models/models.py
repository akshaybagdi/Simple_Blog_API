from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    """Model to hold Comment Information for a specific Post"""

    post = models.ForeignKey(
        "posts.Post",
        related_name="comments",
        on_delete=models.CASCADE,
        help_text="The post this comment belongs to",
    )  # ForeignKey to the Post model
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="The user who authored this comment"
    )  # ForeignKey to the User model
    content = models.TextField(
        help_text="The content of the comment"
    )  # TextField to store the content of the comment
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="The date and time when the comment was created"
    )  # Automatically set when the comment is created
    updated_at = models.DateTimeField(
        auto_now=True, help_text="The date and time when the comment was last updated"
    )  # Automatically set when the comment is updated

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"  # String representation of the comment

    class Meta:
        db_table = "blog_comment"  # Custom table name for the database
        verbose_name = "Comment"  # Singular name for the model
        verbose_name_plural = "Comments"  # Plural name for the model
