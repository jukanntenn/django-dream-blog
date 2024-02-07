from tutorials.models import Category, Tutorial
from tutorials.tests.factories import CategoryFactory, MaterialFactory, TutorialFactory
from users.models import User


def run():
    names = ["Django", "Vue", "React"]
    for name in names:
        CategoryFactory(name=name)

    print(f"Created {len(names)} tutorial categories")

    author = User.objects.get(username="admin")
    for category in Category.objects.all():
        TutorialFactory.create_batch(3, category=category, author=author)

    print(f"Created 9 tutorials")

    for tutorial in Tutorial.objects.all():
        MaterialFactory.create_batch(10, tutorial=tutorial)

    print(f"Created 90 tutorial materials")
