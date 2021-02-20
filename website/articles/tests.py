from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory

from . import PREFERRED_LANGUAGE_EMPTY_LIST_MESSAGE, EMPTY_LIST_MESSAGE
from .models import Article
from .serializers import ArticleSerializer

User = get_user_model()


class TestArticles(APITestCase):

    def setUp(self):
        """
        Creates a couple users as well as a few articles
        """
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='testman', email='test.man@example.com', password='MegaPassword1234')
        self.user.set_password('MegaPassword1234')
        self.user.first_name = 'Test'
        self.user.last_name = 'Man'
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        for x in range(1, 11):
            title = 'Test{}'.format(x)
            post = 'Testing phrase for the post #{}'.format(x)
            article_status = 'Draft' if x % 2 == 0 else 'Published'
            language = 'es' if x % 3 == 0 else 'en'
            article = Article(status=article_status, author_id=self.user.id, title=title, post=post, language=language)
            article.save()
        self.user2 = User.objects.create(username='testwoman', email='test.woman@example.com',
                                         password='MegaPassword1234')
        self.user2.set_password('MegaPassword1234')
        self.user2.first_name = 'Test'
        self.user2.last_name = 'Woman'
        self.user2.save()
        self.token2 = Token.objects.create(user=self.user2)
        self.token2.save()
        self.user3 = User.objects.create(username='testfrench', email='test.french@example.com',
                                         password='MegaPassword1234', preferred_language='fr')
        self.user3.set_password('MegaPassword1234')
        self.user3.first_name = 'Test'
        self.user3.last_name = 'French'
        self.user3.save()
        self.token3 = Token.objects.create(user=self.user3)
        self.token3.save()

    def test_article_list(self):
        """
        Tests article listing for a non-logged in user and logged in users.
        """
        url = reverse('api:article-list')
        """ This 1st response should only show published articles for an anonymous user. """
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        """ This 2nd response should show all published articles, and the users own articles. """
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
        response2 = self.client.get(url, format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 10)
        self.client.credentials()
        """ This 3rd response will show the user articles in their preferred language only """
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token2.key))
        response3 = self.client.get(url, format='json')
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response3.data), 3)
        self.client.credentials()
        """ This 4rd response will show the user articles in their preferred language only, which should be empty """
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token3.key))
        response4 = self.client.get(url, format='json')
        self.assertEqual(response4.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response4.data, {'Message': PREFERRED_LANGUAGE_EMPTY_LIST_MESSAGE})
        self.client.credentials()

        articles = Article.objects.filter(status='Published')
        request = self.factory.get('/')
        serializer = ArticleSerializer(articles, context={'request': request}, many=True)
        response = self.client.get(reverse('api:article-list'))
        self.assertEqual(response.data, serializer.data)

    def test_article_creation_update_deletion(self):
        """
        This tests article creation if a user is NOT logged in, then if they ARE logged in
        """
        url = reverse('api:article-list')
        data = {
            'status': 'Draft',
            'title': 'Testing',
            'post': 'Testing Post.',
            'language': 'en'
        }
        data2 = {
            'status': 'Published',
            'title': 'Testing update',
            'post': 'Testing Post update.',
            'language': 'en'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
        response2 = self.client.post(url, data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        response3 = self.client.put(response2.data['url'], data2, format='json')
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        response4 = self.client.delete(url + str(response2.data['id']), format='json')
        self.assertEqual(response4.status_code, status.HTTP_301_MOVED_PERMANENTLY)
        self.client.credentials()

    def test_article_get(self):
        """
        Tests an anonymous user getting a published article, a Draft article, and a logged in user getting their
        own draft article, and a logged in user getting another users draft article
        """
        response = self.client.get('/api/articles/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'status': 'Published', 'author': 'testman', 'title': 'Test1',
                                         'post': 'Testing phrase for the post #1', 'language': 'en',
                                         'publication_date': response.data['publication_date'],
                                         'url': 'http://testserver/api/articles/1/'})
        response2 = self.client.get('/api/articles/2/')
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
        response3 = self.client.get('/api/articles/2/')
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.data, {'id': 2, 'status': 'Draft', 'author': 'testman', 'title': 'Test2',
                                          'post': 'Testing phrase for the post #2', 'language': 'en',
                                          'publication_date': response3.data['publication_date'],
                                          'url': 'http://testserver/api/articles/2/'})
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token2.key))
        response4 = self.client.get('/api/articles/2/')
        self.assertEqual(response4.status_code, status.HTTP_404_NOT_FOUND)

    def test_article_search(self):
        """
        Tests searching of an article for several users, and anonymous user.
        """
        url = reverse('api:article-list') + '?search=Test3'
        articles = Article.objects.filter(title='Test3')
        request = self.factory.get('/')
        serializer = ArticleSerializer(articles, context={'request': request}, many=True)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
        response2 = self.client.get(url, format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data, serializer.data)
        self.assertNotEqual(response2.data, {'Message': PREFERRED_LANGUAGE_EMPTY_LIST_MESSAGE})
        self.client.credentials()
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token2.key))
        response3 = self.client.get(url, format='json')
        self.assertEqual(response3.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(response3.data, serializer.data)
        self.assertEqual(response3.data, {'Message': PREFERRED_LANGUAGE_EMPTY_LIST_MESSAGE})
        self.client.credentials()

    def test_article_filter(self):
        """
        Tests filtering for an article for several users, and anonymous user.
        """
        url = reverse('api:article-list') + '?title=Test3&post=&author__username=&language=es'
        url2 = reverse('api:article-list') + '?title=Test3&post=&author__username=&language=en'
        articles = Article.objects.filter(title='Test3', language='es')
        request = self.factory.get('/')
        serializer = ArticleSerializer(articles, context={'request': request}, many=True)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
        response2 = self.client.get(url, format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data, serializer.data)
        self.assertNotEqual(response2.data, {'Message': EMPTY_LIST_MESSAGE})
        self.client.credentials()
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token2.key))
        response3 = self.client.get(url, format='json')
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.data, serializer.data)
        self.assertNotEqual(response3.data, {'Message': EMPTY_LIST_MESSAGE})
        response4 = self.client.get(url2, format='json')
        self.assertEqual(response4.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(response4.data, serializer.data)
        self.assertEqual(response4.data, {'Message': EMPTY_LIST_MESSAGE})
        self.client.credentials()
