from django.urls import reverse
from posts.models import Post


def test_auto_set_admin_as_post_author(admin_client, admin_user):
    url = reverse("admin:posts_post_add")
    data = {
        "title": "Test Tile",
        "content": "Test content",
        "alerts-alert-content_type-object_id-TOTAL_FORMS": "0",
        "alerts-alert-content_type-object_id-INITIAL_FORMS": "0",
        "alerts-alert-content_type-object_id-MIN_NUM_FORMS": "0",
        "alerts-alert-content_type-object_id-MAX_NUM_FORMS": "1000",
    }
    response = admin_client.post(url, data=data)
    assert response.status_code == 302

    assert Post.objects.count() == 1
    post = Post.objects.all().latest("created_at")
    assert post.author == admin_user
