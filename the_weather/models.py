from django.db import models


class City(models.Model):
    """Creates a table in database that has a column called name"""
    name = models.CharField(max_length=25)

    def __str__(self):
        """ Shows actual city name on dashboard """
        return self.name

    class Meta:
        """Shows the plural of city as cities instead"""
        verbose_name_plural = 'cities'

# In order to make these changes in the database, run
# python manage.py makemigrations
# python manage.py migrate
