from haystack import indexes
from tutorials.models import Tutorial


class TutorialIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Tutorial

    def index_queryset(self, using=None):
        return self.get_model().objects.visible()
