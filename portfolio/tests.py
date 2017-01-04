from django.test import TestCase
from portfolio.models import Category
from django.core.urlresolvers import reverse


# Create your tests here.

class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):

        cat= Category(name='test', views=-1, likes = 0)
        cat.save()
        self.assertEqual((cat.views>=0), True)

    def test_slug_line_creation(self):

        cat=Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')




class IndexViewTests(TestCase):


    def test_index_view_with_no_categories(self):

        def add_cat(name, views, likes):
            c = Category.objects.get_or_create(name=name)[0]
            c.views = views
            c.likes = likes
            c.save()
            return c

        add_cat('test',1,1)
        add_cat('temp',1,1)
        add_cat('tmp',1,1)
        add_cat('tmp test temp',1,1)


        response= self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tmp test temp")

        num_cats =len(response.context['categories'])
        self.assertEqual(num_cats, 4)
