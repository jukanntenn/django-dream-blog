from dream_blog.webtools.forms import DjangoSecretKeyCreateForm


class TestDjangoSecretKeyCreateForm:
    def test_valid_empty_form(self):
        form = DjangoSecretKeyCreateForm(data={})
        assert form.is_valid()

    def test_create_secret_key_default(self):
        form = DjangoSecretKeyCreateForm(data={})
        assert form.is_valid()
        key = form.create_secret_key()
        assert len(key) == 50

    def test_create_secret_key_with_prefix(self):
        form = DjangoSecretKeyCreateForm(data={"key_prefix": "test"})
        assert form.is_valid()
        key = form.create_secret_key()
        assert key.startswith("test")
        assert len(key) == 50

    def test_create_secret_key_with_suffix(self):
        form = DjangoSecretKeyCreateForm(data={"key_suffix": "end"})
        assert form.is_valid()
        key = form.create_secret_key()
        assert key.endswith("end")
        assert len(key) == 50

    def test_create_secret_key_with_prefix_and_suffix(self):
        form = DjangoSecretKeyCreateForm(data={"key_prefix": "pre", "key_suffix": "suf"})
        assert form.is_valid()
        key = form.create_secret_key()
        assert key.startswith("pre")
        assert key.endswith("suf")
        assert len(key) == 50
