from django.test import TestCase

from frontend.models import Exhibit


class HomepageTest(TestCase):
    def test_homepage_is_available(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

    def test_homepage_renders_exhibit_from_database(self):
        Exhibit.objects.create(
            title='Mostra test',
            slug='mostra-test',
            authors='Autore Test',
            excerpt_it='Estratto',
            description_it='<p>Descrizione</p>',
            excerpt_en='Excerpt',
            description_en='<p>Description</p>',
            address='Roma',
            begun_at='2026-01-10',
            ended_at='2026-01-12',
        )
        response = self.client.get('/')
        self.assertContains(response, 'Mostra test')
        self.assertContains(response, 'Autore Test')


class AdminLoginTest(TestCase):
    def test_admin_login_is_available(self):
        response = self.client.get('/admin/login/')
        self.assertEqual(200, response.status_code)
