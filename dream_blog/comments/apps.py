from django.apps import AppConfig


class CommentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dream_blog.comments"

    def ready(self) -> None:
        from dream_blog.comments.moderation import CommentModerator, moderator
        from dream_blog.posts.models import Post
        from dream_blog.tutorials.models import Material

        moderator.register(Post, CommentModerator)
        moderator.register(Material, CommentModerator)
