from django.test import TestCase

# Create your tests here.
from django.urls import resolve, reverse
from .views import index, detail
from .models import Post, User, Category


class HomeTests(TestCase):
    def setUp(self):
        User.objects.create_user('william902', '2587193036@qq.com', '123456')
        Category.objects.create(name='力量举')
        self.post_1 = Post.objects.create(title='test1', body='test1', category=Category.objects.get(name='力量举'),
                            author=User.objects.get(username='william902'))
        Post.objects.create(title='test2', body='test2', category=Category.objects.get(name='力量举'),
                            author=User.objects.get(username='william902'))
        Post.objects.create(title='test3', body='test3', category=Category.objects.get(name='力量举'),
                            author=User.objects.get(username='william902'))
        self.response = self.client.get(reverse('index'))

    def test_index_url_resolves_index_view(self):
        view = resolve('/')
        self.assertEquals(view.func, index)

    def test_index_view_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)

    def test_index_view_contains_link_to_post_page(self):
        url = reverse('detail', kwargs={'post_id': self.post_1.id})
        self.assertContains(self.response, 'href="{0}"'.format(url))


class PostTests(TestCase):
    def setUp(self):
        User.objects.create_user('william902', '2587193036@qq.com', '123456')
        Category.objects.create(name='力量举')
        Post.objects.create(title='test1', body='test1', category=Category.objects.get(name='力量举'),
                            author=User.objects.get(username='william902'))
        Post.objects.create(title='test2', body='test2', category=Category.objects.get(name='力量举'),
                            author=User.objects.get(username='william902'))
        Post.objects.create(title='test3', body='test3', category=Category.objects.get(name='力量举'),
                            author=User.objects.get(username='william902'))

    def test_post_view_success_status_code(self):
        url = reverse('detail', kwargs={'post_id': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_post_not_found_status_code(self):
        url = reverse('detail', kwargs={'post_id': 952})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_post_page_contain_link_to_index_page(self):
        url = reverse('index')
        response = self.client.get('/posts/1/')
        self.assertContains(response, 'href="{0}"'.format(url))

    # def test_post_url_resolves_detail_view(self):
    #     view = resolve('posts/1')
    #     self.assertEquals(view.func, detail('1'))


class CreateNewPostTest(TestCase):
    def test_csrf(self):
        response = self.client.get(reverse('create_post'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_post_invalid_post(self):
        url = reverse('create_post')
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)


class UserModelTest(TestCase):
    def test_verbose_name(self):
        url = reverse('account_signup')
        response = self.client.get(url)
        self.assertContains(response, '用户名')
