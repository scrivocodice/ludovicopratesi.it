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
            excerpt='Estratto',
            description='<p>Descrizione</p>',
            address='Roma',
            begun_at='2026-01-10',
            ended_at='2026-01-12',
        )
        response = self.client.get('/')
        self.assertContains(response, 'Mostra test')
        self.assertContains(response, 'Autore Test')

    def test_homepage_orders_exhibits_descending(self):
        Exhibit.objects.create(
            title='Mostra meno recente',
            slug='mostra-meno-recente',
            authors='Autore 1',
            excerpt='Prima',
            description='<p>Prima</p>',
            address='Roma',
            begun_at='2025-01-10',
            ended_at='2025-01-12',
        )
        Exhibit.objects.create(
            title='Mostra piu recente',
            slug='mostra-piu-recente',
            authors='Autore 2',
            excerpt='Seconda',
            description='<p>Seconda</p>',
            address='Roma',
            begun_at='2026-01-10',
            ended_at='2026-01-12',
        )

        response = self.client.get('/')
        self.assertContains(
            response,
            'Mostra piu recente',
            html=False,
        )
        self.assertLess(
            response.content.find(b'Mostra piu recente'),
            response.content.find(b'Mostra meno recente'),
        )

    def test_homepage_exhibit_card_opens_modal_from_full_row(self):
        Exhibit.objects.create(
            title='Mostra clickabile',
            slug='card-click',
            authors='Autore Click',
            excerpt='Estratto',
            description='<p>Descrizione</p>',
            address='Roma',
            begun_at='2026-01-10',
            ended_at='2026-01-12',
        )

        response = self.client.get('/')
        self.assertContains(response, 'data-modal-open="#mostra-card-click"', count=1)
        self.assertContains(response, 'role="button"', count=1)
        self.assertContains(response, 'aria-controls="mostra-card-click"', count=1)


class AdminLoginTest(TestCase):
    def test_admin_login_is_available(self):
        response = self.client.get('/admin/login/')
        self.assertEqual(200, response.status_code)
