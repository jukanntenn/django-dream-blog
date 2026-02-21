from django.apps import AppConfig


class CommentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "comments"

    def ready(self) -> None:
        from comments.moderation import CommentModerator, moderator
        from posts.models import Post
        from tutorials.models import Material

        moderator.register(Post, CommentModerator)
        moderator.register(Material, CommentModerator)
