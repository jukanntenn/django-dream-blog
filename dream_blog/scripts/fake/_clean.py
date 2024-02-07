from django.conf import settings
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()


def run():
    if not settings.DEBUG:
        warning_msg = (
            "You are not in development environment. "
            "This script will DELETE ALL DATA in your database. "
            "If you really want to continue this script, please input 'yEs'. "
            "Make sure you know what you are doing!"
        )
        print(warning_msg)
        prompt = input("Please input 'yEs' to continue")
        if prompt != "yEs":
            print("Unexpected input, return!")
            return

    User.objects.all().delete()
    Post.objects.all().delete()
    print("Cleaned database")
