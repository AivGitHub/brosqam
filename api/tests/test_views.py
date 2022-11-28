from http import HTTPStatus

from django.test import TestCase


class ApiViewsCase(TestCase):
    def setUp(self):
        pass

    def test_health_endpoint(self):
        response_get = self.client.get('/health/')
        response_post = self.client.post('/health/')

        self.assertEqual(response_get.content.decode(), '', 'Body is not empty')

        self.assertEqual(response_get.status_code, HTTPStatus.OK, 'GET returned not %s' % HTTPStatus.OK)
        self.assertEqual(
            response_post.status_code, HTTPStatus.METHOD_NOT_ALLOWED,
            'POST returned not %s' % HTTPStatus.METHOD_NOT_ALLOWED
        )
