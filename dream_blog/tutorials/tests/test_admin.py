from django.urls import reverse

from dream_blog.tutorials.models import Tutorial


def test_auto_set_admin_as_tutorial_author(admin_client, admin_user):
    url = reverse("admin:tutorials_tutorial_add")
    data = {
        "title": "Test Tutorial",
        "slug": "test-tutorial",
        "content": "Test content",
        "status": Tutorial.STATUS.writing,
        "alerts-alert-content_type-object_id-TOTAL_FORMS": "0",
        "alerts-alert-content_type-object_id-INITIAL_FORMS": "0",
        "alerts-alert-content_type-object_id-MIN_NUM_FORMS": "0",
        "alerts-alert-content_type-object_id-MAX_NUM_FORMS": "1000",
    }
    response = admin_client.post(url, data=data)
    assert response.status_code == 302

    assert Tutorial.objects.count() == 1
    tutorial = Tutorial.objects.all().latest("created_at")
    assert tutorial.author == admin_user
