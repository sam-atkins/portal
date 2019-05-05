from django.test import TestCase

from home.utils import split_strings


class Utils(TestCase):
    def test_split_strings(self):
        location = "wsz__warsaw"
        output = split_strings(original_string=location)
        assert output == ["wsz", "warsaw"]
