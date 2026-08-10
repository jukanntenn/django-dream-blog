from typing import TYPE_CHECKING

from django import forms
from django_comments.forms import CommentForm

from dream_blog.comments import get_model

if TYPE_CHECKING:
    from dream_blog.comments.models import Comment


class TreeCommentForm(CommentForm):
    parent = forms.IntegerField(required=False, widget=forms.HiddenInput)

    def __init__(self, target_object, parent: "Comment | None" = None, data=None, initial=None, **kwargs):
        self.parent = parent
        if initial is None:
            initial = {}

        if parent:
            initial.update({"parent": parent.pk})

        super().__init__(target_object, data=data, initial=initial, **kwargs)
        self.fields["email"].required = False
        self.fields["name"].required = False
        self.fields["honeypot"].widget.input_type = "hidden"

    def get_comment_model(self):
        return get_model()

    def get_comment_create_data(self, site_id=None, **kwargs):
        d = super().get_comment_create_data(site_id=site_id)
        # todo: validate parent
        d["parent_id"] = self.cleaned_data["parent"]
        return d

    def check_for_duplicate_comment(self, new):
        return new
