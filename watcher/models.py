from datetime import datetime

from django.conf import settings
from django.db import models


class FavoriteServiceModel(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = 'Favorite service'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    datetime = models.DateTimeField('Publication date', default=datetime.now)
    name = models.TextField('Service name', unique=True, max_length=512)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
