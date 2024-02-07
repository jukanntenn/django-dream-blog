from django.urls import reverse
from posts.models import Post


def test_auto_set_admin_as_post_author(admin_client, admin_user):
    url = reverse("admin:posts_post_add")
    data = {
        "title": "Test Tile",
        "content": "Test content",
    }
    response = admin_client.post(url, data=data)
    assert response.status_code == 302

    assert Post.objects.count() == 1
    post = Post.objects.all().latest("created_at")
    assert post.author == admin_user
