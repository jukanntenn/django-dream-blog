import pytest

from dream_blog.posts.models import Post
from dream_blog.posts.tests.factories import PostFactory
from dream_blog.tutorials.tests.factories import CategoryFactory, MaterialFactory, TutorialFactory
from dream_blog.users.models import User


@pytest.fixture
def user() -> User:
    return User.objects.create_user(username="user", password="password", email="user@example.com")


@pytest.fixture
def post(user: User) -> Post:
    return PostFactory(author=user, title="Test Title")


@pytest.fixture
def tutorial_category():
    return CategoryFactory(name="test")


@pytest.fixture
def tutorial(user: User, tutorial_category) -> Post:
    return TutorialFactory(
        title="Test tutorial",
        author=user,
        category=tutorial_category,
    )


@pytest.fixture
def material(tutorial) -> Post:
    return MaterialFactory(
        title="Test material",
        tutorial=tutorial,
    )
