from django import template
from django.urls import reverse

register = template.Library()


@register.filter
def entry_url(entry):
    """
    Generate URL for an index entry dictionary.

    Args:
        entry: Dictionary with keys: id, type, parent_slug

    Returns:
        URL string for the entry's detail page
    """
    entry_type = entry.get('type')
    pk = entry.get('id')
    parent_slug = entry.get('parent_slug')

    if entry_type == 'p':
        return reverse('posts:detail', kwargs={'pk': pk})
    elif entry_type == 'a':
        return reverse(
            'columns:article_detail',
            kwargs={'slug': parent_slug, 'pk': pk}
        )
    elif entry_type == 'm':
        return reverse(
            'tutorials:material_detail',
            kwargs={'slug': parent_slug, 'pk': pk}
        )
    return '#'
