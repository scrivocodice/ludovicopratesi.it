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

    def test_homepage_decodes_html_entities_in_exhibit_text(self):
        Exhibit.objects.create(
            title='&lsquo;Mostra&rsquo; &amp; prova',
            slug='mostra-entita-html',
            authors='Autore&nbsp;Test',
            excerpt='&lsquo;Ci eleviamo sollevando gli altri&rsquo; di&nbsp;Marinella Senatore, &egrave; la seconda opera.',
            description='<p>&lsquo;Ci eleviamo sollevando gli altri&rsquo; di&nbsp;Marinella Senatore, &egrave; la seconda opera.</p>',
            address='Roma&nbsp;Centro',
            begun_at='2026-01-10',
            ended_at='2026-01-12',
        )

        response = self.client.get('/')
        self.assertContains(response, "‘Mostra’ &amp; prova", html=False)
        self.assertContains(response, 'Autore Test', html=False)
        self.assertContains(
            response,
            '‘Ci eleviamo sollevando gli altri’ di Marinella Senatore, è la seconda opera.',
            html=False,
        )
        self.assertContains(response, 'Roma Centro', html=False)
        self.assertNotContains(response, '&lsquo;', html=False)
        self.assertNotContains(response, '&nbsp;', html=False)
        self.assertNotContains(response, '&egrave;', html=False)


class AdminLoginTest(TestCase):
    def test_admin_login_is_available(self):
        response = self.client.get('/admin/login/')
        self.assertEqual(200, response.status_code)
