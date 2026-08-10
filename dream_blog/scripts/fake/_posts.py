from dream_blog.posts.tests.factories import PostFactory
from dream_blog.users.models import User

_NUM_POSTS = 100


def run():
    author = User.objects.get(username="admin")
    PostFactory.create_batch(_NUM_POSTS, author=author)
    print(f"Created {_NUM_POSTS} posts")
