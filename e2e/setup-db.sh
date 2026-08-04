#!/usr/bin/env bash
# e2e database setup: migrate and seed test data.
# Usage: bash e2e/setup-db.sh
set -euo pipefail

echo "[e2e] Running migrations..."
cd "$(dirname "$0")/.."
uv run python manage.py migrate --run-syncdb

echo "[e2e] Creating test data..."
uv run python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

# Create test user if not exists
if not User.objects.filter(username='testuser').exists():
    User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com'
    )
    print('[e2e] Created test user: testuser / testpass123')
else:
    print('[e2e] Test user already exists')

# Create superuser for admin tests
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        password='adminpass123',
        email='admin@example.com'
    )
    print('[e2e] Created admin user: admin / adminpass123')
else:
    print('[e2e] Admin user already exists')

user = User.objects.get(username='testuser')
admin = User.objects.get(username='admin')
now = timezone.now()

# --- Posts ---
from posts.models import Post
if Post.objects.count() == 0:
    Post.objects.create(
        title='First Blog Post',
        content='# Hello World\n\nThis is the first blog post content.',
        excerpt='A short excerpt for the first post.',
        publish_date=now - timedelta(days=2),
        author=admin,
    )
    Post.objects.create(
        title='Second Blog Post',
        content='# Another Post\n\nMore content here with **markdown**.',
        excerpt='Excerpt for the second post.',
        publish_date=now - timedelta(days=1),
        author=admin,
    )
    Post.objects.create(
        title='Draft Post',
        content='# Draft\n\nThis post is not published yet.',
        publish_date=None,
        author=admin,
    )
    print('[e2e] Created 3 posts')
else:
    print('[e2e] Posts already exist')

# --- Tutorials ---
from tutorials.models import Category, Tutorial, Material
if Tutorial.objects.count() == 0:
    cat = Category.objects.create(name='Python Basics')
    t1 = Tutorial.objects.create(
        title='Getting Started with Python',
        slug='getting-started-python',
        excerpt='Learn Python basics step by step.',
        content='# Getting Started\n\nPython is a great language.',
        status=Tutorial.STATUS.completed,
        author=admin,
        category=cat,
    )
    Material.objects.create(
        title='Installing Python',
        content='# Install Python\n\nDownload from python.org.',
        publish_date=now - timedelta(days=3),
        tutorial=t1,
    )
    Material.objects.create(
        title='Your First Script',
        content='# First Script\n\nprint(\"Hello, World!\")',
        publish_date=now - timedelta(days=2),
        tutorial=t1,
    )
    t2 = Tutorial.objects.create(
        title='Django Tutorial',
        slug='django-tutorial',
        excerpt='Build web apps with Django.',
        content='# Django\n\nDjango is a web framework.',
        status=Tutorial.STATUS.writing,
        author=admin,
        category=cat,
    )
    Material.objects.create(
        title='Django Setup',
        content='# Setup Django\n\npip install django',
        publish_date=now - timedelta(days=1),
        tutorial=t2,
    )
    print('[e2e] Created tutorials with materials')
else:
    print('[e2e] Tutorials already exist')

# --- Columns ---
from columns.models import Column, Article
if Column.objects.count() == 0:
    col = Column.objects.create(
        title='Weekly Picks',
        slug='weekly-picks',
        excerpt='Curated weekly recommendations.',
        content='# Weekly Picks\n\nBest content of the week.',
        author=admin,
    )
    Article.objects.create(
        title='Pick #1: Great Article',
        content='# Pick #1\n\nThis is a great article.',
        publish_date=now - timedelta(days=5),
        column=col,
    )
    Article.objects.create(
        title='Pick #2: Another Gem',
        content='# Pick #2\n\nAnother excellent read.',
        publish_date=now - timedelta(days=3),
        column=col,
    )
    print('[e2e] Created columns with articles')
else:
    print('[e2e] Columns already exist')

# --- Favorites (Issues) ---
from dream_blog.favorites.models import Issue, Favorite
if Issue.objects.count() == 0:
    issue = Issue.objects.create(
        number=1,
        pub_date=now - timedelta(days=7),
        description='First issue of weekly favorites.',
        creator=admin,
    )
    Favorite.objects.create(
        issue=issue,
        title='Interesting Python Tool',
        description='A tool that makes Python development easier.',
        url='https://example.com/tool',
        rank=1,
    )
    Favorite.objects.create(
        issue=issue,
        title='Django Best Practices',
        description='Tips for Django developers.',
        url='https://example.com/django-tips',
        rank=2,
    )
    print('[e2e] Created issues with favorites')
else:
    print('[e2e] Issues already exist')

# --- Newsletters ---
from dream_blog.newsletters.models import Subscription
if Subscription.objects.count() == 0:
    Subscription.objects.create(
        email='subscriber@example.com',
        confirmed=True,
        active=True,
    )
    print('[e2e] Created newsletter subscription')
else:
    print('[e2e] Subscriptions already exist')

print('[e2e] Seed data complete.')
"

echo "[e2e] Setup complete. Run tests: cd e2e && npm test"
