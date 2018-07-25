from django.test import TestCase

# Create your tests here.
from django.urls import resolve, reverse
from .views import index, detail
from .models import Post, User, Category


class HomeTests(TestCase):
    def setUp(self):
        User.objects.create_user('william902', '2587193036@qq.com', '123456')
        Category.objects.create(name='力量举')
        Post.objects.create(title='test1', body='test1', category=Category.objects.get(name='力量举'),
                            author=User.objects.get(username='william902'))
        Post.objects.create(title='test2', body='test2', category=Category.objects.get(name='力量举'),
                            author=User.objects.get(username='william902'))
        Post.objects.create(title='test3', body='test3', category=Category.objects.get(name='力量举'),
                            author=User.objects.get(username='william902'))

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, index)

    def test_home_view_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        # self.assertContains(response, )
