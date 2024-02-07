from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_str


# Take from https://github.com/brack3t/django-braces
class SetHeadlineMixin:
    """
    Define a `headline` context item as a view attribute
    """

    headline = None  # Default the headline to none

    def get_context_data(self, **kwargs):
        """Add the headline to the context"""
        kwargs = super().get_context_data(**kwargs)
        kwargs.update({"headline": self.get_headline()})
        return kwargs

    def get_headline(self):
        """Fetch the headline from the instance"""
        if self.headline is None:
            class_name = self.__class__.__name__
            raise ImproperlyConfigured(
                f"{class_name} is missing the headline attribute. "
                f"Define {class_name}.headline, or override {class_name}.get_headline()."
            )
        return force_str(self.headline)
