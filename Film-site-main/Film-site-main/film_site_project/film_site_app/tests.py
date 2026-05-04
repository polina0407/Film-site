from django.test import TestCase
from django.test import TestCase
from .models import Genre

class GenreModelTest(TestCase):
    def setUp(self):

        Genre.objects.create(title="Django для профі",
    author = "Guido")


def test_string_representation(self):
    genre = Genre.objects.get(id=1)
    self.assertEqual(str(genre), "Django для профі")

