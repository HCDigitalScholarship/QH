from django.db import models

# Create your models here.
class Book(models.Model):
    authors = models.ManyToManyField('Author')
    title = models.CharField(max_length=200, help_text='Enter the title of the book')
    publisher = models.CharField(max_length=200, help_text='Enter the publisher of the book', blank=True)
    published_date = models.DateField(blank=True)
    identifier = models.CharField(max_length=200, help_text='Enter the title of the book')
    language = models.CharField(max_length=200, null=True)
    categories = models.ManyToManyField('Category',blank=True)
    text = models.TextField(blank=True)
    page_count= models.IntegerField(blank=True)
    thumbnail = models.URLField(blank=True)
    language = models.CharField(max_length=200, blank=True)
    raw_json = models.TextField(blank=True)


    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f'{self.title}'

class Author(models.Model):
    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}'


class Category(models.Model):
    """Model representing a book genre"""
    name = models.CharField(max_length=200,)

    def __str__(self):
        return self.name
