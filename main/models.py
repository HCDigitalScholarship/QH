from django.db import models

# Create your models here.
class Item(models.Model):
    authors = models.ManyToManyField('Author')
    title = models.CharField(max_length=200, help_text='Enter the title of the book')
    publisher = models.CharField(max_length=200, help_text='Enter the publisher of the book', blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    identifier = models.CharField(max_length=200, help_text='Enter the title of the book', blank=True, null=True)
    language = models.CharField(max_length=200, null=True, blank=True)
    categories = models.ManyToManyField('Category',blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    page_count= models.IntegerField(blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)
    language = models.CharField(max_length=200, blank=True, null=True)
    raw_json = models.TextField(blank=True,null=True)
    print_type = models.CharField(max_length=200, blank=True, null=True)

    def parse_json(self):
        # publisher = data['publisher'],
        # published_date = parse_date(data['publishedDate']),
        # identifier = data['industryIdentifiers'][0]['identifier'],
        # language = data['language'],
        # page_count= data['pageCount'],
        # thumbnail = data['imageLinks']['thumbnail'],
        #print_type = data['printType'],
        self.save()
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
