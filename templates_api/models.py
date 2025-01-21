# templates_api/models.py
from django.db import models

class EmailTemplate(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    footer = models.TextField()
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
