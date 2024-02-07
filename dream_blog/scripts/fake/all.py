from django.db import transaction

from . import _clean, _posts, _superuser, _tutorials


def run():
    with transaction.atomic():
        _clean.run()
        _superuser.run()
        _posts.run()
        _tutorials.run()

        print("Done!")
