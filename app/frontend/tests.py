from django.test import TestCase
from frontend.models import Exhibit

class WebRouteTest(TestCase):
    routes = ()

    def test_successful(self):
        """
        Tests route successful
        """
        for route in self.routes:
            response = self.client.get(route)
            self.assertEqual(200, response.status_code, "route %s NOT OK" % route)

class HomepageTest(WebRouteTest):
    routes = ("/it/", "/en/")

class ExhibitListTest(WebRouteTest):
    routes = ("/en/exhibits/", "/it/mostre/")

class ExhibitShowTest(WebRouteTest):
    routes = ("/en/exhibit/prova/", "/it/mostra/prova/",)

    def test_successful(self):
        Exhibit.objects.create(
            title = "prova",
            slug = "prova",
            begun_at = "2013-10-10",
            ended_at = "2013-10-12",
        )
        super(ExhibitShowTest, self).test_successful()

class ResumeTest(WebRouteTest):
    routes = ("/en/resume/", "/it/curriculum-vitae/")

class ContactsTest(WebRouteTest):
    routes = ("/en/contacts/", "/it/contatti/", \
        "/en/contacts/successful-message-sent/",
        "/it/contatti/messaggio-inviato-con-successo/",
    )
