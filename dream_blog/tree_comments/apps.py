from django.apps import AppConfig


class TreeCommentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tree_comments"

    def ready(self) -> None:
        from posts.models import Post
        from tree_comments.moderation import CommentModerator, moderator
        from tutorials.models import Material

        moderator.register(Post, CommentModerator)
        moderator.register(Material, CommentModerator)
