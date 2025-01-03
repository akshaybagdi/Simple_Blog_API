from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    """Model to hold Post Info"""

    title = models.CharField(
        _("Title"), max_length=255, help_text=_("Enter the title of the post.")
    )
    abstract = models.TextField(
        _("Abstract"),
        blank=True,
        help_text=_("Enter a short summary or abstract for the post."),
    )
    content = models.TextField(
        _("Content"), help_text=_("Enter the full content of the post.")
    )
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        help_text=_("Select the author of the post."),
    )
    publication_date = models.DateTimeField(
        _("Publication Date"),
        auto_now_add=True,
        help_text=_("The date and time when the post was created."),
    )
    status = models.CharField(
        _("Status"),
        max_length=10,
        choices=(("draft", "Draft"), ("published", "Published")),
        default="draft",
        help_text=_("Set the status of the post (e.g., Draft or Published)."),
    )
    journal = models.CharField(
        _("Journal"),
        max_length=255,
        blank=True,
        help_text=_("Enter the name of the journal, if applicable."),
    )
    volume = models.CharField(
        _("Volume"),
        max_length=50,
        blank=True,
        help_text=_("Enter the volume number, if applicable."),
    )
    website = models.URLField(
        _("Website"),
        max_length=200,
        blank=True,
        help_text=_("Enter a URL related to the post, if applicable."),
    )

    def __str__(self):
        return (
            self.title
        )  # Return the title of the post when the post object is printed

    class Meta:
        db_table = "blog_post"  # Custom table name for the database
        verbose_name = _("Post")  # Singular name for the model (used in admin)
        verbose_name_plural = _("Posts")  # Plural name for the model (used in admin)
