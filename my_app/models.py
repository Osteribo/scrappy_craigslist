from django.db import models

# Create your models here.

class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    # this will set the of the search to the string entered in the search bar
    def __str__(self):
        return '{}'.format(self.search)
    class Meta:
        verbose_name_plural = 'Searches'