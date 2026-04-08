from django.db import models


class HTMLField(models.TextField):
    """
    Minimal compatibility field used by historical migrations.
    """
